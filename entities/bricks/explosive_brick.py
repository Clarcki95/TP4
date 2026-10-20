"""
But : Définition des briques explosives.
Auteur : Tristan GUIEU
Date : 13/10/26
TODO : détruire les briques dans un carré de rayon radius.
"""

from config import RESOURCES_DIR
from entities.bricks.brick import Brick


class ExplosiveBrick(Brick):
    """Brique explosive dont l'effet reste à implémenter."""

    def __init__(self, pos_x, pos_y, sound_manager) -> None:
        super().__init__(pos_x, pos_y, sound_manager)

        self.pv = 4
        self.radius = 1
        self.texture = RESOURCES_DIR / "bricks" / "explosive_brick_v2.webp"
        self.score = 30

    def on_death(self) -> int:
        super().sound_manager.sound("explosion")
        return super().on_death()
