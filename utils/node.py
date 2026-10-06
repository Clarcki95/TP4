"""
Fichier: node.py
But: Implémentation d'un noeud dans une liste chaînée.
Auteur: Nino BELAOUD
"""

class Node:
    """Noeud"""

    def __init__(self, value):
        """
        Initialise un noeud avec une valeur.

        Args:
            value: La valeur du noeud.
        """
        self.value = value
        self.next: Node | None = None

    def set_next(self, next):
        """
        Définit le noeud suivant.

        Args:
            next (Node | None): Le noeud suivant.
        """
        self.next = next
