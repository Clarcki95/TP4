"""
Fichier : level_manager.py
But : Sélection des niveaux et gestion des briques de la partie en cours.
Auteur : Nino BELAOUD
"""

import tkinter as tk
from functools import partial

from entities.bricks.brick import Brick
from game.levels.level import Level
from utils.list import List


class LevelManager:
    """Conserve les niveaux disponibles et les briques actuellement en jeu."""

    def __init__(self, canvas: tk.Canvas, sound_manager) -> None:
        """Prépare le premier niveau sans encore créer ses widgets."""
        self.selected_level: Level | None = None

        self.canvas = canvas
        self.sound_manager = sound_manager
        # Seules les briques de la partie en cours sont modifiées ou détruites.
        self.bricks = List()

        # Les définitions des niveaux restent disponibles après un redémarrage.
        self.levels = List()

        # ========== Niveau 1 ==========
        level_1_bricks = List()

        for pos_x in (400, 800, 600, 1000, 1200):
            # partial mémorise les arguments sans construire le widget immédiatement.
            level_1_bricks.add(partial(Brick, pos_x, 150, self.sound_manager, 1, self.canvas))

        level_1 = Level("Niveau 1", level_1_bricks)

        self.levels.add(level_1)
        # ===============================

        self.select_level(0)

    def select_level(self, level_id: int) -> None:
        """
        Sélectionne un niveau sans démarrer de partie.

        Args:
            level_id (int): Index du niveau dans la liste des niveaux disponibles.

        Raises:
            IndexError: Si l'index ne correspond à aucun niveau.
        """
        self.selected_level = self.levels.get(level_id)

    def get_selected_level(self) -> Level:
        """
        Retourne la définition du niveau sélectionné.

        Raises:
            ValueError: Si aucun niveau n'est sélectionné.
        """
        if self.selected_level is None:
            raise ValueError("No selected level")

        return self.selected_level

    def get_bricks(self) -> List:
        """Retourne la liste des briques encore présentes dans la partie."""
        return self.bricks

    def remove_brick(self, index: int) -> None:
        """
        Retire de la liste une brique dont le widget a déjà été détruit.

        Args:
            index (int): Position de la brique dans la liste des briques actives.

        Raises:
            IndexError: Si l'index est invalide ou si la liste est vide.
        """
        self.bricks.remove(index)

    def init_level(self) -> None:
        """
        Crée et affiche les briques du niveau sélectionné.

        La partie précédente doit être nettoyée avec clear_level() avant cet appel.
        """
        level = self.get_selected_level()

        # Recréer les widgets et leurs points de vie à chaque nouvelle partie.
        self.bricks = level.new_bricks()
        for brick in self.bricks.to_list():
            brick.create()

    def clear_level(self) -> None:
        """Détruit les briques actives en conservant la définition du niveau."""
        for brick in self.bricks.to_list():
            brick.destroy()

        # Oublier les widgets détruits pour permettre plusieurs nettoyages successifs.
        self.bricks = List()
