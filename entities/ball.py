"""
Fichier: ball.py
But: Balle
Auteur: Nino BELAOUD
"""
import tkinter as tk

from physics.hitbox import Hitbox

# Taille de la balle en px
BALL_SIZE = 10

class Ball:
    def __init__(self, canvas: tk.Canvas, start_x: float, start_y: float, start_vx: float, start_vy: float):
        self.canvas = canvas

        self.hitbox = Hitbox(start_x, start_y, BALL_SIZE, BALL_SIZE)
        self.hitbox.set_velocity(start_vx, start_vy)

        self.drawing = self.canvas.create_oval(self.hitbox.x_min, self.hitbox.y_min, self.hitbox.x_max, self.hitbox.y_max, fill="blue")

    def update(self):
        if self.drawing is not None:
            self.hitbox.update_movement()
            self.canvas.coords(self.drawing, self.hitbox.x_min, self.hitbox.y_min, self.hitbox.x_max, self.hitbox.y_max)
