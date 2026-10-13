"""
Fichier: racket.py
But: Raquette du joueur
Auteur: Tristan GUIEU
"""

import tkinter as tk

from physics.hitbox import Hitbox

SPEED = 20
WIDTH = 150
HEIGHT = 30
BOTTOM_MARGIN = 100


class Racket:
    """Raquette rectangulaire contrôlée par le joueur."""

    def __init__(self, canvas: tk.Canvas) -> None:
        self.hitbox = Hitbox(50, 800, WIDTH, HEIGHT)
        self.canvas = canvas
        self.create()

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

    def move_left(self) -> None:
        """Déplace la raquette vers la gauche si son bord gauche est positif."""
        if 0 < self.canvas.coords(self.rect)[0]:
            self.canvas.move(self.rect, -SPEED, 0)
            self.sync_hitbox()

    def move_right(self) -> None:
        """Déplace la raquette vers la droite si son bord droit est dans le canevas."""
        if self.canvas.coords(self.rect)[0] + WIDTH < self.canvas.winfo_width():
            self.canvas.move(self.rect, SPEED, 0)
            self.sync_hitbox()

    def sync_hitbox(self) -> None:
        """Recentre la hitbox sur le rectangle après un déplacement."""
        self.hitbox.set_pos(
            self.canvas.coords(self.rect)[0] + WIDTH / 2,
            self.canvas.coords(self.rect)[1] + HEIGHT / 2,
        )
