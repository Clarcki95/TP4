"""
But : Définition des briques accélératrices.
Auteur : Tristan GUIEU
Date : 13/10/26
TODO : compléter l'effet de on_death.
"""

import tkinter as tk

from config import RESOURCES_DIR
from entities.ball import Ball
from entities.bricks.brick import Brick


class AcceleratorBrick(Brick):
    """Brique accélératrice"""

    def __init__(self, pos_x, pos_y, sound_manager, canvas: tk.Canvas) -> None:
        super().__init__(pos_x, pos_y, sound_manager, 2, canvas)

        self.pv = 2
        self.score = 15
        self.texture = RESOURCES_DIR / "bricks" / "accelerator_brick_v2.webp"

    def on_death(self) -> int:
        return super().on_death()

    def compute_collision(self, ball: Ball) -> bool:
        will_collide = super().compute_collision(ball)

        if will_collide:
            ball.speed_up()

        return will_collide
