"""
But : Ce fichier contient la classe déifnissant les briques de base.
Auteur : Tristan GUIEU
Date : 13/10/26
ToDo : 
"""

import tkinter as tk
import physics.hitbox as hitbox

class Brick(tk.Label):
    def __init__(self, posX, posY):
        super().__init__()

        self.pv = 1
        self.texture = "./Ressources/Bricks/brick.webp"
        self.score = 10

        self.hitbox = hitbox.Hitbox(posX, posY, 100, 50)

        self.create()

    def create(self):
        """
        But : créer la brique
        Entrée : self, classe
        Sortie : aucune
        """
        image = tk.PhotoImage(file = self.texture)
        self.config(image = image)
        self.pack()


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