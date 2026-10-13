"""
But : Définition des briques accélératrices.
Auteur : Tristan GUIEU
Date : 13/10/26
TODO : compléter l'effet de on_death.
"""

from entities.bricks.brick import Brick


class AcceleratorBrick(Brick):
    """Brique accélératrice dont l'effet reste à implémenter."""

    def __init__(self) -> None:
        super().__init__()

        self.pv = 2
        self.score = 15
        self.texture = "./ressources/bricks/accelerator_brick.webp"

    def on_death(self) -> int:
        return super().on_death()
