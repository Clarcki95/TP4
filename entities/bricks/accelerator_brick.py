"""
But : Ce fichier contient la classe déifnissant les briques accélératrices.
Auteur : Tristan GUIEU
Date : 13/10/26
ToDo : onDeath
"""

import entities.bricks.brick as B

class Accelerator_Brick(B.Brick):
    def __init__(self):
        super().__init__()

        self.pv = 2
        self.score = 15
        self.texture = "./ressources/bricks/accelerator_brick.webp"

    def onDeath(self):
        return super().onDeath()