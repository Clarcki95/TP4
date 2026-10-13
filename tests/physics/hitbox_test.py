"""
Fichier: tests/physics/hitbox_test.py
But: Tests unitaires pour la classe Hitbox.
Auteur: Nino BELAOUD
"""
from math import isclose

from physics.hitbox import Hitbox

print("==============================")
print("physics/hitbox.py")

# Initialisation : la position correspond au centre du rectangle.
hitbox = Hitbox(3, -2, 4, 6)

assert hitbox.x == 3
assert hitbox.y == -2
assert hitbox.width == 4
assert hitbox.height == 6
assert hitbox.x_min == 1
assert hitbox.x_max == 5
assert hitbox.y_min == -5
assert hitbox.y_max == 1
assert hitbox.vx == 0
assert hitbox.vy == 0

# Changement de position : toutes les limites sont recalculées.
hitbox.set_pos(-4, 5)

assert hitbox.x == -4
assert hitbox.y == 5
assert hitbox.x_min == -6
assert hitbox.x_max == -2
assert hitbox.y_min == 2
assert hitbox.y_max == 8
assert hitbox.width == 4
assert hitbox.height == 6

# Changement de vitesse sans déplacement de la hitbox.
hitbox.set_velocity(2.5, -3.5)

assert hitbox.vx == 2.5
assert hitbox.vy == -3.5
assert hitbox.x == -4
assert hitbox.y == 5
assert hitbox.x_min == -6
assert hitbox.x_max == -2
assert hitbox.y_min == 2
assert hitbox.y_max == 8

# Rebonds sur les quatre faces avec une composante tangentielle non nulle.
# X augmente vers la droite et Y vers le haut.
for vx, vy, obstacle_x, obstacle_y, width, height, x, y, new_vx, new_vy in [
    (10, 2, 6, 0, 2, 10, 4, 0.8, -10, 2),  # Vers la droite.
    (-10, 2, -6, 0, 2, 10, -4, 0.8, 10, 2),  # Vers la gauche.
    (2, 10, 0, 6, 10, 2, 0.8, 4, 2, -10),  # Vers le haut.
    (2, -10, 0, -6, 10, 2, 0.8, -4, 2, 10),  # Vers le bas.
]:
    mobile = Hitbox(0, 0, 2, 2)
    obstacle = Hitbox(obstacle_x, obstacle_y, width, height)
    mobile.set_velocity(vx, vy)
    obstacle.set_velocity(3, -7)

    assert mobile.compute_collision(obstacle) is True
    assert isclose(mobile.x, x)
    assert isclose(mobile.y, y)
    assert mobile.vx == new_vx
    assert mobile.vy == new_vy
    assert isclose(mobile.x_min, x - 1)
    assert isclose(mobile.x_max, x + 1)
    assert isclose(mobile.y_min, y - 1)
    assert isclose(mobile.y_max, y + 1)
    assert mobile.width == 2
    assert mobile.height == 2
    assert mobile.vx ** 2 + mobile.vy ** 2 == vx ** 2 + vy ** 2

    # L'obstacle est considéré comme fixe, même si sa vitesse est non nulle.
    assert obstacle.x == obstacle_x
    assert obstacle.y == obstacle_y
    assert obstacle.x_min == obstacle_x - width / 2
    assert obstacle.x_max == obstacle_x + width / 2
    assert obstacle.y_min == obstacle_y - height / 2
    assert obstacle.y_max == obstacle_y + height / 2
    assert obstacle.vx == 3
    assert obstacle.vy == -7

# Contacts dans les quatre angles : les deux composantes sont inversées.
for direction_x, direction_y in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
    mobile = Hitbox(0, 0, 2, 2)
    obstacle = Hitbox(6 * direction_x, 6 * direction_y, 2, 2)
    mobile.set_velocity(10 * direction_x, 10 * direction_y)

    assert mobile.compute_collision(obstacle) is True
    assert mobile.x == 4 * direction_x
    assert mobile.y == 4 * direction_y
    assert mobile.vx == -10 * direction_x
    assert mobile.vy == -10 * direction_y

# Entrées presque simultanées : en dessous de la tolérance, rebond d'angle.
# Au-delà, seule la composante de l'axe du dernier contact est inversée.
for offset_y, new_vx in [(0.00005, -10), (0.0002, 10)]:
    mobile = Hitbox(0, 0, 2, 2)
    obstacle = Hitbox(6, 6 + offset_y, 2, 2)
    mobile.set_velocity(10, 10)

    assert mobile.compute_collision(obstacle) is True
    assert isclose(mobile.x, 4 + offset_y)
    assert isclose(mobile.y, 4 + offset_y)
    assert mobile.vx == new_vx
    assert mobile.vy == -10

# Déplacement rapide : l'obstacle est détecté même s'il serait traversé.
mobile = Hitbox(0, 0, 2, 2)
obstacle = Hitbox(6, 0, 2, 10)
mobile.set_velocity(100, 0)

assert mobile.compute_collision(obstacle) is True
assert mobile.x == 4
assert mobile.y == 0
assert mobile.vx == -100
assert mobile.vy == 0

# Contact dès le départ (t = 0) ou exactement à la fin (t = 1).
for obstacle_x, contact_x in [(2, 0), (12, 10)]:
    mobile = Hitbox(0, 0, 2, 2)
    obstacle = Hitbox(obstacle_x, 0, 2, 2)
    mobile.set_velocity(10, 0)

    assert mobile.compute_collision(obstacle) is True
    assert mobile.x == contact_x
    assert mobile.y == 0
    assert mobile.vx == -10
    assert mobile.vy == 0

# Absence de collision : ni la position, ni les limites, ni la vitesse
# du mobile ne doivent être modifiées.
for vx, vy, obstacle_x, obstacle_y in [
    (0, 0, 6, 0),  # Mobile immobile.
    (1, 0, 6, 0),  # Obstacle trop loin pour être atteint.
    (0, 1, 0, 6),  # Même cas sur Y.
    (-10, 0, 6, 0),  # Le mobile s'éloigne de l'obstacle à droite.
    (10, 0, -6, 0),  # Le mobile s'éloigne de l'obstacle à gauche.
    (0, -10, 0, 6),  # Le mobile s'éloigne de l'obstacle au-dessus.
    (0, 10, 0, -6),  # Le mobile s'éloigne de l'obstacle en dessous.
    (-10, 0, 2, 0),  # Contact initial, mais déplacement vers l'extérieur.
    (10, 0, 0, 3),  # Axe Y immobile et projections séparées.
    (10, 0, 0, -3),
    (10, 0, 0, 2),  # Axe Y immobile et bords seulement en contact.
    (10, 0, 0, -2),
    (0, 10, 3, 0),  # Axe X immobile et projections séparées.
    (0, 10, -3, 0),
    (0, 10, 2, 0),  # Axe X immobile et bords seulement en contact.
    (0, 10, -2, 0),
    (10, 10, 3, 8),  # Intervalles de contact disjoints sur X et Y.
    (10, 10, 8, 3),
    (10, 0, 0, 0),  # Chevauchement initial ignoré par l'implémentation.
    (10, 0, 1, 1),  # Chevauchement initial partiel également ignoré.
]:
    mobile = Hitbox(0, 0, 2, 2)
    obstacle = Hitbox(obstacle_x, obstacle_y, 2, 2)
    mobile.set_velocity(vx, vy)

    assert mobile.compute_collision(obstacle) is False
    assert mobile.x == 0
    assert mobile.y == 0
    assert mobile.x_min == -1
    assert mobile.x_max == 1
    assert mobile.y_min == -1
    assert mobile.y_max == 1
    assert mobile.vx == vx
    assert mobile.vy == vy
    assert obstacle.x == obstacle_x
    assert obstacle.y == obstacle_y
    assert obstacle.vx == 0
    assert obstacle.vy == 0

print("✅ Tests validés")
print("==============================")
