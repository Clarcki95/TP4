"""
Fichier: hitbox.py
But: Implémentation d'une hitbox avec collision suivant l'algorithme SWEPT AABB.
Auteur: Nino BELAOUD
"""
from math import inf

TOLERANCE = 10e-6


class Hitbox:
    """Rectangle mobile dont la position correspond à son centre."""

    def __init__(self, x: float, y: float, width: float, height: float):
        # Taille
        self.width = width
        self.height = height

        # Position
        self.x = 0
        self.y = 0

        # Vitesse
        self.vx = 0
        self.vy = 0

        # Coins
        self.x_max = 0
        self.x_min = 0
        self.y_max = 0
        self.y_min = 0

        self.set_pos(x, y)

    def update_movement(self):
        """
        Mettre à jour la position de la hitbox en fonction de sa vitesse.
        """
        self.set_pos(self.x + self.vx, self.y + self.vy)

    def set_pos(self, x: float, y: float):
        """
        Définir la position de la hitbox.
        """
        self.x = x
        self.y = y
        self.x_min = x - self.width / 2
        self.y_min = y - self.height / 2
        self.x_max = x + self.width / 2
        self.y_max = y + self.height / 2

    def set_velocity(self, vx: float, vy: float):
        """
        Définir la vitesse de la hitbox.
        """
        self.vx = vx
        self.vy = vy

    def compute_collision(self, hitbox):
        """
        Détecter la collision avec une autre hitbox et appliquer le rebond.

        Args:
            hitbox (Hitbox): La hitbox fixe avec laquelle détecter la collision.

        Returns:
            bool: True si une collision est détectée, False sinon.
        """
        # ================================
        # DÉTECTION DE LA COLLISION
        # ================================
        # Chevauchement initial
        if (
            self.x_min < hitbox.x_max
            and self.x_max > hitbox.x_min
            and self.y_min < hitbox.y_max
            and self.y_max > hitbox.y_min
        ):
            return False

        # Aucune vitesse, pas de collision
        if self.vx == 0 and self.vy == 0:
            return False

        # Calcul des temps d'entrée et de sortie sur chaque axe.

        # Axe X
        t_entry_x = 0
        t_exit_x = 0

        if self.vx > 0:
            # Par la gauche
            t_entry_x = (hitbox.x_min - self.x_max) / self.vx
            t_exit_x = (hitbox.x_max - self.x_min) / self.vx
        elif self.vx < 0:
            # Par la droite
            t_entry_x = (hitbox.x_max - self.x_min) / self.vx
            t_exit_x = (hitbox.x_min - self.x_max) / self.vx
        else:
            if self.x_max <= hitbox.x_min or self.x_min >= hitbox.x_max:
                return False

            t_entry_x = -inf
            t_exit_x = inf

        # Axe Y
        t_entry_y = 0
        t_exit_y = 0

        if self.vy > 0:
            # Par le haut
            t_entry_y = (hitbox.y_min - self.y_max) / self.vy
            t_exit_y = (hitbox.y_max - self.y_min) / self.vy
        elif self.vy < 0:
            # Par le bas
            t_entry_y = (hitbox.y_max - self.y_min) / self.vy
            t_exit_y = (hitbox.y_min - self.y_max) / self.vy
        else:
            if self.y_max <= hitbox.y_min or self.y_min >= hitbox.y_max:
                return False

            t_entry_y = -inf
            t_exit_y = inf

        t_entry = max(t_entry_x, t_entry_y)
        t_exit = min(t_exit_x, t_exit_y)

        # S'il n'y a pas de collision.
        will_collide = t_entry <= t_exit and 0 <= t_entry <= 1 and t_exit >= 0

        if not will_collide:
            return False

        # ================================
        # CALCUL DU REBOND
        # ================================

        # Position de la hitbox au contact
        new_x = self.x + t_entry * self.vx
        new_y = self.y + t_entry * self.vy

        # Nouvelle vitesse
        new_vx = self.vx
        new_vy = self.vy

        if abs(t_entry_x - t_entry_y) <= TOLERANCE:
            # Collision dans un angle
            new_vx = -self.vx
            new_vy = -self.vy
        elif t_entry_x > t_entry_y:
            # Collision sur l'axe X
            new_vx = -self.vx
        else:
            # Collision sur l'axe Y
            new_vy = -self.vy

        # print("x:", new_x, "y:", new_y)
        # print("vx:", new_vx, "vy:", new_vy)
        # print("t_entry_x:", t_entry_x, "t_entry_y:", t_entry_y)

        # Applique la nouvelle position et vitesse
        self.set_pos(new_x, new_y)
        self.set_velocity(new_vx, new_vy)

        return True
