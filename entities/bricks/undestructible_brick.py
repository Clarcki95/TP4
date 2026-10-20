"""
But : Définition des briques indestructibles.
Auteur : Tristan GUIEU
Date : 13/10/26
"""

from config import RESOURCES_DIR
from entities.bricks.brick import Brick


class UndestructibleBrick(Brick):
    """Brique initialisée avec un nombre de points de vie négatif."""

    def __init__(self, pos_x, pos_y, sound_manager, master=None) -> None:
        super().__init__(pos_x, pos_y, sound_manager, -1, master)

        self.pv = -1
        self.texture = RESOURCES_DIR / "bricks" / "undestructible_brick_v2.webp"
