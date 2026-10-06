"""
Fichier: list.py
But: Implémentation d'une pile.
Auteur: Nino BELAOUD
"""
from utils.list import List


class Stack:
    """Pile"""

    def __init__(self):
        """Initialise une pile vide à l'aide d'une liste chaînée."""
        self.list = List()

    def get_size(self):
        """
        Retourne le nombre d'éléments présents dans la pile.

        Returns:
            int: Nombre d'éléments dans la pile.
        """
        return self.list.size

    def is_empty(self):
        """
        Vérifie si la pile est vide.

        Returns:
            bool: True si la pile est vide, False sinon.
        """
        return self.get_size() == 0

    def head(self):
        """
        Récupère la valeur situé au sommet de la pile.

        Returns:
            any | None: Valeur au sommet de la pile, ou None si la pile est vide.
        """
        if self.is_empty():
            return None

        return self.list.get(self.list.size - 1)

    def push(self, value):
        """
        Ajoute un élément au sommet de la pile.

        Args:
            value: Valeur de l'élément à empiler.
        """
        self.list.add(value)

    def pop(self):
        """
        Retire et retourne la valeur situé au sommet de la pile.

        Returns:
            any: Valeur retirée du sommet de la pile.

        Raises:
            IndexError: Si la pile est vide.
        """
        if self.is_empty():
            raise IndexError("Stack is empty")

        value = self.head()
        self.list.remove()

        return value
