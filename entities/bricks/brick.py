"""
But : Définition des briques de base.
Auteur : Tristan GUIEU
Date : 13/10/26
"""

import tkinter as tk

from PIL import Image, ImageTk

from config import RESOURCES_DIR
from entities.ball import Ball
from physics.hitbox import Hitbox

BRICK_WIDTH = 100
BRICK_HEIGHT = 50


class Brick(tk.Label):
    """Brique affichée dans un label et associée à une hitbox."""

    def __init__(self, pos_x, pos_y, sound_manager, pv=1, master=None) -> None:
        """
        Prépare une brique sans encore charger sa texture ni l'afficher.

        Args:
            pos_x (float): Abscisse du centre de la brique.
            pos_y (float): Ordonnée du centre de la brique.
            pv (int): Nombre initial de points de vie.
            master (tk.Misc | None): Widget parent de la brique.
        """
        super().__init__(master, borderwidth=0, highlightthickness=0)

        self.pv = pv
        self.texture = RESOURCES_DIR / "bricks" / "brick.webp"
        self.score = 10

        self.sound_manager = sound_manager

        self.hitbox = Hitbox(pos_x, pos_y, BRICK_WIDTH, BRICK_HEIGHT)
        # Le gestionnaire de niveaux appelle create() au démarrage de la partie.

    def create(self) -> None:
        """Charge la texture et place la brique au centre de sa hitbox."""
        with Image.open(self.texture) as image:
            self.image = ImageTk.PhotoImage(
                image.resize((int(self.hitbox.width), int(self.hitbox.height))), master=self
            )
        self.config(image=self.image)
        self.place(x=self.hitbox.x, y=self.hitbox.y, anchor=tk.CENTER)

    def on_touch(self) -> None:
        """Retire un point de vie et détruit la brique lorsqu'elle atteint zéro."""
        self.pv -= 1

        if self.pv == 0:
            self.on_death()

    def on_death(self) -> int:
        """Détruit le label et retourne le score associé à la brique."""
        self.sound_manager.sound("death")
        self.destroy()
        return self.score

    def compute_collision(self, ball: Ball) -> bool:
        return ball.hitbox.compute_collision(self.hitbox)
