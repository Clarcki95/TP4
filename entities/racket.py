"""
Fichier: racket.py
But: Raquette du joueur
Auteur: Tristan GUIEU
"""

import tkinter as tk

from physics.hitbox import Hitbox

# Vitesse maximale (px/tick)
VELOCITY_MAX = 17
# Acceleration (px/tick^2)
ACCELERATION = 8
# Décélération au relâchement (px/tick^2)
FRICTION = 5

WIDTH = 150
HEIGHT = 30
BOTTOM_MARGIN = 100


class Racket:
    """Raquette rectangulaire contrôlée par le joueur."""

    def __init__(self, canvas: tk.Canvas) -> None:
        self.hitbox = Hitbox(50, 800, WIDTH, HEIGHT)
        self.canvas = canvas
        self.acceleration = ACCELERATION
        self.velocity = 0
        self.create()
        self.sync_hitbox()

    def create(self) -> None:
        """Dessine la raquette au bas du canevas."""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        self.rect = self.canvas.create_rectangle(
            width / 2 - WIDTH / 2,
            height - BOTTOM_MARGIN - HEIGHT,
            width / 2 + WIDTH / 2,
            height - BOTTOM_MARGIN,
            fill="white",
        )

    def update(self, direction: int = 0) -> None:
        """Avance d'un tick selon la direction (-1, 0 ou 1), sans sortir du canevas."""
        if direction:
            self.velocity += direction * self.acceleration
        elif self.velocity > 0:
            self.velocity = max(0, self.velocity - FRICTION)
        elif self.velocity < 0:
            self.velocity = min(0, self.velocity + FRICTION)

        # Clamp la vitesse entre V_MAX
        self.velocity = max(-VELOCITY_MAX, min(self.velocity, VELOCITY_MAX))

        # Empêcher la raquette de sortir du canevas
        left, _, right, _ = self.canvas.coords(self.rect)
        max_left = max(0, self.canvas.winfo_width() - (right - left))
        next_left = max(0, min(left + self.velocity, max_left))

        self.canvas.move(self.rect, next_left - left, 0)

        # Arrêter la raquette si elle atteint les bords du canevas
        if next_left == 0 or next_left == max_left:
            self.velocity = 0

        # Synchroniser la hitbox
        self.sync_hitbox()

    def sync_hitbox(self) -> None:
        """Recentre la hitbox sur le rectangle après un déplacement."""
        self.hitbox.set_pos(
            self.canvas.coords(self.rect)[0] + WIDTH / 2,
            self.canvas.coords(self.rect)[1] + HEIGHT / 2,
        )
