"""
Fichier: ball.py
But: Balle
Auteur: Nino BELAOUD
"""
import time
import tkinter as tk

from physics.hitbox import Hitbox
from utils.list import List

# Taille de la balle en px
BALL_SIZE = 20

# Durée de l'effet de vitesse en s
EFFECT_SPEED_DURATION_S = 5

class Ball:
    """Balle dont le dessin suit la position de la hitbox."""

    def __init__(
        self,
        canvas: tk.Canvas,
        start_x: float,
        start_y: float,
        start_vx: float,
        start_vy: float,
    ) -> None:
        self.canvas = canvas

        self.speed_effects = List()

        self.hitbox = Hitbox(start_x, start_y, BALL_SIZE, BALL_SIZE)
        self.hitbox.set_velocity(start_vx, start_vy)

        self.drawing = self.canvas.create_oval(
            self.hitbox.x_min,
            self.hitbox.y_min,
            self.hitbox.x_max,
            self.hitbox.y_max,
            fill="blue",
        )

    def update(self) -> None:
        """Avance la hitbox puis actualise le dessin de la balle."""
        if self.drawing is not None:
            self.handle_movement()

        self.handle_speed_decrease()

    def handle_movement(self) -> None:
        self.hitbox.update_movement()
        self.canvas.coords(
            self.drawing,
            self.hitbox.x_min,
            self.hitbox.y_min,
            self.hitbox.x_max,
            self.hitbox.y_max,
        )

    def speed_up(self) -> None:
        self.hitbox.set_velocity(self.hitbox.vx * 1.20, self.hitbox.vy * 1.20)
        self.speed_effects.add(time.time())

    def handle_speed_decrease(self) -> None:
        remove_index = List()

        for i in range(self.speed_effects.size):
            if time.time() - self.speed_effects.get(i) > EFFECT_SPEED_DURATION_S:
                remove_index.add(i)
                self.hitbox.set_velocity(self.hitbox.vx / 1.20, self.hitbox.vy / 1.20)

        for i in remove_index.to_list():
            self.speed_effects.remove(i)
