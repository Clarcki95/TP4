"""Effets préchargés, déclenchés directement dans le moteur audio Windows."""

import atexit

from config import RESOURCES_DIR
from sound.windows_audio import WindowsAudio


class Sound_manager:
    def __init__(self) -> None:
        self._audio = WindowsAudio()
        self.sounds = {}
        try:
            for name in ("bounce_racket", "bounce", "death", "victory", "defeat", "explosion"):
                self.sounds[name] = self._audio.load(RESOURCES_DIR / "sounds" / f"{name}.wav")
        except Exception:
            self.close()
            raise
        atexit.register(self.close)

    def sound(self, sound_name):
        sound = self.sounds.get(sound_name)
        if sound is not None:
            sound.play()

    def close(self):
        self._audio.close()
        self.sounds.clear()
        atexit.unregister(self.close)
