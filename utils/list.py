"""
Fichier: list.py
But: Implémentation d'une liste simplement chaînée.
Auteur: Nino BELAOUD
"""

from utils.node import Node


class List:
    """Liste simplement chaînée."""

    def __init__(self):
        """Initialise une liste chaînée vide."""
        self.first = None
        self.size = 0

    def add(self, value, index: int | None = None):
        """
        Ajoute un élément à une position donnée dans la liste.

        Si aucun index n'est précisé, l'élément est ajouté à la fin.

        Args:
            value: Valeur de l'élément à ajouter.
            index (int | None): Position d'insertion.
                Par défaut, la fin de la liste.

        Raises:
            IndexError: Si l'index est hors des limites autorisées.
        """
        new_node = Node(value)

        # Si l'index n'est pas précisé, on ajoute à la fin.
        if index is None:
            index = self.size

        # Vérifier que l'index est valide.
        if index < 0 or index > self.size:
            raise IndexError("Index out of range")

        # Si la liste est vide.
        if self.first is None:
            self.first = new_node
            self.size += 1
            return

        if index == 0:
            # Insérer au début.
            new_node.set_next(self.first)
            self.first = new_node

        elif index == self.size:
            # Insérer à la fin.
            previous_node = self.get_node(index - 1)
            previous_node.set_next(new_node)

        else:
            # Insérer entre deux éléments.
            previous_node = self.get_node(index - 1)
            next_node = self.get_node(index)

            previous_node.set_next(new_node)
            new_node.set_next(next_node)

        self.size += 1

    def remove(self, index: int | None = None):
        """
        Supprime un élément à une position donnée dans la liste.

        Si aucun index n'est précisé, le dernier élément est supprimé.

        Args:
            index (int | None): Position de l'élément à supprimer.
                Par défaut, le dernier élément.

        Raises:
            IndexError: Si la liste est vide ou si l'index est invalide.
        """
        # Si l'index n'est pas précisé, supprimer le dernier élément.
        if index is None:
            index = self.size - 1

        # Vérifier que l'index est valide.
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")

        if index == 0:
            # Supprimer le premier élément.
            if self.first is not None:
                self.first = self.first.next
            else:
                raise IndexError("Index out of range")

        elif index == self.size - 1:
            # Supprimer le dernier élément.
            previous_node = self.get_node(index - 1)
            previous_node.set_next(None)

        else:
            # Supprimer un élément intermédiaire.
            previous_node = self.get_node(index - 1)
            next_node = self.get_node(index + 1)

            previous_node.set_next(next_node)

        self.size -= 1

    def get_node(self, index: int):
        """
        Récupère le noeud situé à une position donnée.

        Args:
            index (int): Position du nœud à récupérer.

        Returns:
            Node: Noeud situé à l'index demandé.

        Raises:
            IndexError: Si l'index est hors des limites de la liste.
        """
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")

        current = self.first

        if current is None:
            raise IndexError("Index out of range")

        for _ in range(index):
            if current.next is None:
                raise IndexError("Index out of range")

            current = current.next

        return current

    def get(self, index: int):
        """
        Récupère la valeur d'un noeud à une position donnée.

        Args:
            index (int): Position du noeud à récupérer.

        Returns:
            Any: Valeur du noeud à l'index demandé.
        """
        node = self.get_node(index)
        return node.value

    def to_list(self):
        """
        Convertit la liste chaînée en liste Python.

        Returns:
            list: Liste contenant les valeurs des nœuds
                dans leur ordre d'apparition.
        """
        result = []
        current = self.first

        # Parcourir tous les nœuds.
        while current is not None:
            result.append(current.value)
            current = current.next

        return result
