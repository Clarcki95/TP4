"""
But : Définition des briques indestructibles.
Auteur : Tristan GUIEU
Date : 13/10/26
"""

from entities.bricks.brick import Brick


class UndestructibleBrick(Brick):
    """Brique initialisée avec un nombre de points de vie négatif."""

    def __init__(self, pos_x, pos_y) -> None:
        super().__init__(pos_x, pos_y)

        self.pv = -1
        self.texture = "./ressources/bricks/undestructible_brick.webp"
