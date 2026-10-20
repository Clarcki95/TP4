"""
Fichier : level.py
But : Définition d'un niveau.
Auteur : Nino BELAOUD
"""

from utils.list import List


class Level:
    """Définition d'un niveau immuable."""

    def __init__(self, level_name: str, brick_factories: List) -> None:
        """
        Mémorise le nom du niveau et les fonctions créant ses briques.

        Args:
            level_name (str): Nom affiché pour le niveau.
            brick_factories (List): Fonctions sans argument retournant chacune
                une nouvelle brique, sans encore l'afficher.
        """
        self.level_name = level_name
        # Conserver des constructeurs : un widget détruit ne peut pas être réutilisé.
        self.brick_factories = brick_factories

    def get_level_name(self) -> str:
        """Retourne le nom du niveau."""
        return self.level_name

    def new_bricks(self) -> List:
        """
        Crée les briques du niveau avec leurs points de vie initiaux.

        Returns:
            List: Nouveaux widgets à afficher avec leur méthode create().
        """
        bricks = List()
        for factory in self.brick_factories.to_list():
            bricks.add(factory())
        return bricks
