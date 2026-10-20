"""Dimensions, temporisation et ressources communes au jeu."""

import tkinter as tk
from pathlib import Path

_root = tk.Tk()
_root.withdraw()

GAME_WIDTH = _root.winfo_screenwidth()
GAME_HEIGHT = _root.winfo_screenheight()

_root.destroy()

TICK_RATE = 100
TICK_DURATION_MS = int(1000 / TICK_RATE)

RESOURCES_DIR = Path(__file__).resolve().parent / "ressources"

ASSIGNED_KEYS = {
    "left": "q",
    "right": "d",
    "toggle_menu": "Escape",
    "exit_game": "Delete",
}