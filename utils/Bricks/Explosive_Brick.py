"""
But : Ce fichier contient la classe déifnissant les briques explosives.
Auteur : Tristan GUIEU
Date : 13/10/26
ToDo : détruire les briques dans un carré de <radius>
"""

import Brick as B

class Explosive_Brick(B.Brick):
    def __init__(self, posX, posY):
        super().__init__(posX, posY)

        self.pv = 4
        self.radius = 1
        self.texture = "./Ressources/Bricks/explosive_brick.webp"
        self.score = 30

    def onDeath(self):
        return super().onDeath()