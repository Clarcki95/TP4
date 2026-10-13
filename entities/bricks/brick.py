"""
But : Ce fichier contient la classe déifnissant les briques de base.
Auteur : Tristan GUIEU
Date : 13/10/26
ToDo :
"""

from entities.ball import Ball
import physics.hitbox as hitbox

import tkinter as tk

from pathlib import Path
from PIL import Image, ImageTk

class Brick(tk.Label):
    def __init__(self, posX, posY, master=None):
        super().__init__(master, borderwidth=0, highlightthickness=0)

        self.pv = 1
        self.texture = Path(__file__).resolve().parents[2] / "ressources" / "bricks" / "brick.webp"
        self.score = 10

        self.hitbox = hitbox.Hitbox(posX, posY, 100, 50)

        self.create()

    def create(self):
        """
        But : créer la brique
        Entrée : self, classe
        Sortie : aucune
        """
        # TODO: Fix error
        with Image.open(self.texture) as image:
            self.image = ImageTk.PhotoImage(
                image.resize((self.hitbox.width, self.hitbox.height)), master=self
            )
        self.config(image=self.image)
        self.place(x=self.hitbox.x, y=self.hitbox.y, anchor=tk.CENTER)


    def onTouch(self):
        """
        But : définir une action lorsque la brique est touchée
        Entrée : self, classe
        Sortie : aucune
        """
        self.pv -= 1

        if self.pv == 0:
            self.onDeath()

    def onDeath(self):
        """
        But : définir une cation lors de la destruction de l'objet
        Entrée : self, classe
        Sortie : score, int
        """
        self.destroy()
        return self.score

    def compute_collision(self, ball: Ball) -> bool:
        return ball.hitbox.compute_collision(self.hitbox)
