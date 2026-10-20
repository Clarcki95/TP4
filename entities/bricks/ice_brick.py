"""Brique glacée réduisant les frottements de la raquette à sa destruction."""

import tkinter as tk
from collections.abc import Callable

from config import RESOURCES_DIR
from entities.bricks.brick import Brick


class IceBrick(Brick):
    """Brique dont la destruction déclenche un effet de glace temporaire."""

    def __init__(
        self, pos_x, pos_y, sound_manager, canvas: tk.Canvas,
        on_freeze: Callable[[], None],
    ) -> None:
        super().__init__(pos_x, pos_y, sound_manager, 1, canvas)
        self.score = 15
        self.texture = RESOURCES_DIR / "bricks" / "ice_brick.webp"
        self.on_freeze = on_freeze

    def on_death(self) -> int:
        """Gèle la raquette uniquement lorsque la brique est cassée."""
        self.on_freeze()
        return super().on_death()
