"""
Fichier: wall.py
But: Représente un mur
Auteur: Nino BELAOUD
"""

import tkinter as tk

from entities.ball import Ball
from physics.hitbox import Hitbox


class Wall:
    def __init__(self, canvas: tk.Canvas, x: float, y: float, width: float, height: float, bouncy: bool):
        self.canvas = canvas
        self.hitbox = Hitbox(x, y, width, height)
        self.rectangle_id = canvas.create_rectangle(x - width / 2, y - height / 2, x + width / 2, y + height / 2, fill="green")
        self.bouncy = bouncy

    def is_bouncy(self) -> bool:
        return self.bouncy

    def is_hitting(self, ball: Ball) -> bool:
        return self.hitbox.compute_collision(ball.hitbox)
