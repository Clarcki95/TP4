"""Dimensions, temporisation et ressources communes au jeu."""

from pathlib import Path

GAME_WIDTH = 1600
GAME_HEIGHT = 1000

TICK_RATE = 100
TICK_DURATION_MS = int(1000 / TICK_RATE)

RESOURCES_DIR = Path(__file__).resolve().parent / "ressources"

ASSIGNED_KEYS = {"left": "Left", "right": "Right", "toggle_menu": "Escape", "exit_game": "Delete"}