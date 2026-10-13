"""
But : Ce fichier contient la classe déifnissant les briques indestructibles.
Auteur : Tristan GUIEU
Date : 13/10/26
ToDo : 
"""

import Brick as B

class Undestructible_Brick(B.Brick):
    def __init__(self, posX, posY) :
        super().__init__(posX, posY)

        self.pv = -1
        self.texture = "./Ressources/Bricks/undestructible_brick.webp"