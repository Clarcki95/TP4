"""
Fichier: queue.py
But: Implémentation d'une file.
Auteur: Nino BELAOUD
"""
from utils.list import List


class Queue:
    """File"""

    def __init__(self):
        """Initialise une file vide à l'aide d'une liste."""
        self.list = List()

    def get_size(self):
        """
        Retourne le nombre d'éléments présents dans la file.

        Returns:
            int: Nombre d'éléments dans la file.
        """
        return self.list.size

    def is_empty(self):
        """
        Vérifie si la file est vide.

        Returns:
            bool: True si la file est vide, False sinon.
        """
        return self.list.size == 0

    def head(self):
        """
        Récupère la valeur situé en tête de file sans le retirer.

        Returns:
            Node | None: Valeur situé en tête de file,
                ou None si la file est vide.
        """
        if self.is_empty():
            return None

        return self.list.get(0)

    def enqueue(self, value):
        """
        Ajoute un élément à la fin de la file.

        Args:
            value: Valeur de l'élément à enfiler.
        """
        self.list.add(value)

    def dequeue(self):
        """
        Retire et retourne la valeur situé en tête de file.

        Returns:
            Node: Valeur retirée de la tête de file.

        Raises:
            IndexError: Si la file est vide.
        """
        if self.is_empty():
            raise IndexError("Queue is empty")

        value = self.head()
        self.list.remove(0)

        return value
