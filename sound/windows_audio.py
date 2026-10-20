"""Accès minimal à XAudio2, inclus dans Windows 10 et 11.

Le moteur Windows garde les WAV en mémoire et effectue lui-même la lecture.
Aucun thread ou callback audio Python ne tourne pendant la partie.
"""

import ctypes as ct
import wave
from functools import partial


class _WaveFormat(ct.Structure):
    _pack_ = 1
    _fields_ = [
        ("tag", ct.c_uint16),
        ("channels", ct.c_uint16),
        ("rate", ct.c_uint32),
        ("bytes_per_second", ct.c_uint32),
        ("alignment", ct.c_uint16),
        ("bits", ct.c_uint16),
        ("extra_size", ct.c_uint16),
    ]


class _Buffer(ct.Structure):
    _pack_ = 1
    _fields_ = [
        ("flags", ct.c_uint32),
        ("size", ct.c_uint32),
        ("data", ct.c_void_p),
        ("play_begin", ct.c_uint32),
        ("play_length", ct.c_uint32),
        ("loop_begin", ct.c_uint32),
        ("loop_length", ct.c_uint32),
        ("loop_count", ct.c_uint32),
        ("context", ct.c_void_p),
    ]


class _VoiceState(ct.Structure):
    _pack_ = 1
    _fields_ = [
        ("context", ct.c_void_p),
        ("queued", ct.c_uint32),
        ("samples", ct.c_uint64),
    ]


def _check(result):
    if result < 0:
        raise OSError(f"XAudio2 : erreur 0x{result & 0xFFFFFFFF:08X}")


def _method(pointer, index, result, *arguments):
    """Lie une méthode de l'interface native définie dans xaudio2.h."""
    table = ct.cast(pointer, ct.POINTER(ct.POINTER(ct.c_void_p))).contents
    function = ct.WINFUNCTYPE(result, ct.c_void_p, *arguments)(table[index])
    return partial(function, pointer)


class WindowsAudio:
    def __init__(self):
        self._engine = ct.c_void_p()
        self._master = ct.c_void_p()
        self._sounds = []
        self._ole = ct.WinDLL("ole32")
        self._ole.CoInitializeEx.argtypes = [ct.c_void_p, ct.c_uint32]
        self._ole.CoInitializeEx.restype = ct.c_int32
        result = self._ole.CoInitializeEx(None, 0)
        self._owns_com = result >= 0
        # RPC_E_CHANGED_MODE signifie que l'application a déjà initialisé COM.
        if result != -2147417850:
            _check(result)
        try:
            self._dll = ct.WinDLL("xaudio2_9.dll")
            self._dll.XAudio2Create.argtypes = [
                ct.POINTER(ct.c_void_p),
                ct.c_uint32,
                ct.c_uint32,
            ]
            self._dll.XAudio2Create.restype = ct.c_int32
            _check(self._dll.XAudio2Create(ct.byref(self._engine), 0, 1))
            create_master = _method(
                self._engine,
                7,
                ct.c_int32,
                ct.POINTER(ct.c_void_p),
                ct.c_uint32,
                ct.c_uint32,
                ct.c_uint32,
                ct.c_wchar_p,
                ct.c_void_p,
                ct.c_int32,
            )
            _check(create_master(ct.byref(self._master), 0, 0, 0, None, None, 6))
        except Exception:
            self.close()
            raise

    def load(self, path):
        sound = _Sound(self._engine, path)
        self._sounds.append(sound)
        return sound

    def close(self):
        for sound in self._sounds:
            sound.close()
        self._sounds.clear()
        if self._master:
            _method(self._master, 18, None)()  # DestroyVoice
            self._master = ct.c_void_p()
        if self._engine:
            _method(self._engine, 2, ct.c_uint32)()  # Release
            self._engine = ct.c_void_p()
        if self._owns_com:
            self._ole.CoUninitialize()
            self._owns_com = False


class _Sound:
    def __init__(self, engine, path):
        with wave.open(str(path), "rb") as audio:
            rate, channels = audio.getframerate(), audio.getnchannels()
            width = audio.getsampwidth()
            raw = audio.readframes(audio.getnframes())
        alignment = channels * width
        format = _WaveFormat(
            1, channels, rate, rate * alignment, alignment, width * 8, 0
        )
        # Ces données restent vivantes jusqu'à la destruction de toutes les voix.
        self._data = ct.create_string_buffer(raw)
        self._buffer = _Buffer(0x40, len(raw), ct.cast(self._data, ct.c_void_p))
        self._voices = []
        try:
            for _ in range(4):
                self._voices.append(_Voice(engine, format))
        except Exception:
            self.close()
            raise

    def play(self):
        for voice in self._voices:
            if voice.play(self._buffer):
                break
        # En cas de rafale, ne jamais ajouter un effet derrière un autre.

    def close(self):
        for voice in self._voices:
            voice.close()
        self._voices.clear()


class _Voice:
    def __init__(self, engine, format):
        self._voice = ct.c_void_p()
        create_voice = _method(
            engine,
            5,
            ct.c_int32,
            ct.POINTER(ct.c_void_p),
            ct.POINTER(_WaveFormat),
            ct.c_uint32,
            ct.c_float,
            ct.c_void_p,
            ct.c_void_p,
            ct.c_void_p,
        )
        _check(
            create_voice(
                ct.byref(self._voice), ct.byref(format), 0, 2, None, None, None
            )
        )
        self._start = _method(self._voice, 19, ct.c_int32, ct.c_uint32, ct.c_uint32)
        self._submit = _method(
            self._voice, 21, ct.c_int32, ct.POINTER(_Buffer), ct.c_void_p
        )
        self._get_state = _method(
            self._voice, 25, None, ct.POINTER(_VoiceState), ct.c_uint32
        )
        self._state = _VoiceState()

    def play(self, buffer):
        self._get_state(ct.byref(self._state), 0x100)
        if self._state.queued:
            return False
        _check(self._submit(ct.byref(buffer), None))
        _check(self._start(0, 0))
        return True

    def close(self):
        if self._voice:
            _method(self._voice, 18, None)()
            self._voice = ct.c_void_p()
