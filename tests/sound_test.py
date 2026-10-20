"""Déclenchement audio immédiat, sans périphérique sonore pour ces tests."""

import ctypes as ct
import unittest
from unittest.mock import Mock, patch

from sound.sound_manager import Sound_manager
from sound.windows_audio import _Buffer, _Sound, _Voice, _VoiceState, _WaveFormat


class SoundTest(unittest.TestCase):
    def test_effects_are_preloaded_and_play_does_not_reopen_a_file(self):
        with patch("sound.sound_manager.WindowsAudio") as backend:
            manager = Sound_manager()
        try:
            self.assertEqual(backend.return_value.load.call_count, 3)
            with patch("wave.open", side_effect=AssertionError("Lecture disque")):
                manager.sound("bounce")
            manager.sounds["bounce"].play.assert_called_once()
            manager.sound("unknown")
        finally:
            manager.close()
        self.assertFalse(manager.sounds)

    def test_partial_loading_failure_releases_audio(self):
        with patch("sound.sound_manager.WindowsAudio") as backend:
            backend.return_value.load.side_effect = OSError("Fichier invalide")
            with self.assertRaises(OSError):
                Sound_manager()
            backend.return_value.close.assert_called_once()

    def test_busy_voice_does_not_queue_another_effect(self):
        voice = object.__new__(_Voice)
        voice._state = _VoiceState()
        voice._state.queued = 1
        voice._get_state = Mock()
        voice._submit = Mock(return_value=0)
        voice._start = Mock(return_value=0)
        self.assertFalse(voice.play(_Buffer()))
        voice._submit.assert_not_called()
        voice._state.queued = 0
        self.assertTrue(voice.play(_Buffer()))
        voice._submit.assert_called_once()
        voice._start.assert_called_once_with(0, 0)

    def test_simultaneous_effect_uses_an_idle_voice(self):
        sound = object.__new__(_Sound)
        sound._buffer = _Buffer()
        sound._voices = [Mock(), Mock(), Mock()]
        sound._voices[0].play.return_value = False
        sound._voices[1].play.return_value = True
        sound.play()
        sound._voices[1].play.assert_called_once_with(sound._buffer)
        sound._voices[2].play.assert_not_called()

    def test_native_structures_follow_the_windows_packed_layout(self):
        self.assertEqual(ct.sizeof(_WaveFormat), 18)
        self.assertEqual(ct.sizeof(_Buffer), 28 + 2 * ct.sizeof(ct.c_void_p))
        self.assertEqual(ct.sizeof(_VoiceState), 12 + ct.sizeof(ct.c_void_p))


if __name__ == "__main__":
    unittest.main()
