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
        self.rectangle_id = canvas.create_rectangle(self.hitbox.x_min, self.hitbox.y_min, self.hitbox.x_max, self.hitbox.y_max, fill="green")
        self.canvas.tag_raise(self.rectangle_id)
        self.bouncy = bouncy

    def is_bouncy(self) -> bool:
        return self.bouncy

    def compute_collision(self, ball: Ball) -> bool:
        return ball.hitbox.compute_collision(self.hitbox)
