
from threading import Thread
from playsound import playsound
import winsound

class Sound_manager():
    def __init__(self):
        self.sounds = {"bounce_racket": "bounce_racket", 
                       "bounce": "bounce",
                       "death": "death",
                       "victory": "",
                       "defeat": ""}

    def sound(self, sound_name):
        filename = self.sounds.get(sound_name)

        if filename:
            path = f"./Ressources/sounds/{filename}.wav"

            print(path)

            winsound.PlaySound(
                path,
                winsound.SND_FILENAME | winsound.SND_ASYNC
            )

            print("played")