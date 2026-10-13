# Hitbox, collisions et rebonds

Cette documentation décrit le comportement de la classe `Hitbox`, définie dans
[`physics/hitbox.py`](physics/hitbox.py). Elle représente un rectangle, détecte
son premier contact avec un obstacle fixe pendant un déplacement et applique
un rebond.

## 1. Représentation d'une hitbox

Une **hitbox** est une forme géométrique utilisée pour calculer les collisions
d'un objet. Ici, il s'agit d'un rectangle aligné sur les axes X et Y : on parle
d'**AABB** (*Axis-Aligned Bounding Box*). Le rectangle ne tourne pas.

La position `(x, y)` correspond au **centre** du rectangle. Ses limites sont
calculées à partir de sa largeur et de sa hauteur :

```text
x_min = x - width / 2       x_max = x + width / 2
y_min = y - height / 2      y_max = y + height / 2
```

Le repère est orienté de gauche à droite pour X et du bas vers le haut pour Y.
Ainsi, `x_min` est le bord gauche, `x_max` le bord droit, `y_min` le bord bas
et `y_max` le bord haut :

```text
           x_min                     x_max
             +-------------------------+  y_max
             |                         |
             |        (x, y)           |
             |                         |
             +-------------------------+  y_min
```

| Attributs | Rôle |
| --- | --- |
| `x`, `y` | Coordonnées du centre |
| `width`, `height` | Dimensions du rectangle |
| `x_min`, `x_max`, `y_min`, `y_max` | Limites du rectangle |
| `vx`, `vy` | Composantes du déplacement sur un pas de simulation |

Le constructeur initialise les vitesses à zéro. Utiliser `set_pos(x, y)` pour
déplacer la hitbox : cette méthode met aussi à jour ses limites. Modifier
directement `x` ou `y` laisserait les limites incohérentes. Si les dimensions
changent, il faut également rappeler `set_pos` pour les recalculer.

## 2. Détection des collisions : Swept AABB

Un test de chevauchement à la fin du déplacement peut manquer un obstacle
traversé par un objet rapide. Le **Swept AABB** examine le trajet entier en
calculant les instants d'entrée et de sortie sur chaque axe.

L'appel `mobile.compute_collision(obstacle)` considère `obstacle` comme fixe.
Ses attributs `vx` et `vy` ne sont pas utilisés.

### Vérifications initiales

La méthode renvoie immédiatement `False` dans deux cas :

- Les rectangles se chevauchent déjà strictement sur les deux axes. Ce cas
  n'est pas corrigé par l'implémentation actuelle.
- La hitbox mobile a une vitesse nulle sur les deux axes.

Deux bords qui se touchent ne constituent pas un chevauchement strict.

### Temps d'entrée et de sortie sur X

Le temps d'entrée indique quand les projections des rectangles commencent à
se toucher sur l'axe. Le temps de sortie indique quand elles cessent de se
recouvrir.

Si la hitbox avance vers les X croissants (`vx > 0`) :

```text
t_entry_x = (obstacle.x_min - mobile.x_max) / vx
t_exit_x  = (obstacle.x_max - mobile.x_min) / vx
```

Si elle avance vers les X décroissants (`vx < 0`) :

```text
t_entry_x = (obstacle.x_max - mobile.x_min) / vx
t_exit_x  = (obstacle.x_min - mobile.x_max) / vx
```

Si `vx == 0`, aucune division n'est effectuée :

- Si les projections sur X sont séparées ou se touchent seulement, la méthode
  renvoie `False` : aucun recouvrement sur X ne peut apparaître.
- Sinon, `t_entry_x = -inf` et `t_exit_x = inf`. L'axe X n'impose alors aucune
  limite temporelle au contact.

### Temps d'entrée et de sortie sur Y

Le même calcul s'applique sur Y, en remplaçant `x` par `y` et `vx` par `vy`.
Dans ce repère, une vitesse `vy > 0` correspond à une montée et
`vy < 0` à une descente. Le cas `vy == 0` suit les mêmes règles que sur X.

### Combinaison des deux axes

Pour que les rectangles se rencontrent, leurs projections doivent se recouvrir
sur les deux axes au même moment :

```text
t_entry = max(t_entry_x, t_entry_y)
t_exit  = min(t_exit_x, t_exit_y)
```

On retient l'entrée la plus tardive et la sortie la plus précoce. Une collision
est acceptée si :

```python
t_entry <= t_exit and 0 <= t_entry <= 1 and t_exit >= 0
```

Cela signifie que les intervalles de contact se rencontrent et que le premier
contact se produit pendant le pas étudié. Les contacts à `t = 0` ou `t = 1`
peuvent être acceptés si les autres conditions sont satisfaites.

## 3. Position au contact et rebond

Lorsqu'une collision est détectée, la hitbox mobile est déplacée jusqu'au
point de contact :

```text
new_x = x + t_entry * vx
new_y = y + t_entry * vy
```

La direction du rebond dépend de l'axe sur lequel l'entrée a lieu en dernier :

| Condition | Contact | Nouvelle vitesse |
| --- | --- | --- |
| `abs(t_entry_x - t_entry_y) <= TOLERANCE` | Angle : entrées presque simultanées | `(-vx, -vy)` |
| Sinon, `t_entry_x > t_entry_y` | Face verticale, contact sur X | `(-vx, vy)` |
| Sinon | Face horizontale, contact sur Y | `(vx, -vy)` |

`TOLERANCE = 10e-6`, soit `0.00001`, compare les **temps d'entrée**. Elle ne
représente pas une distance entre les rectangles.

Le rebond inverse une ou deux composantes sans réduire leur valeur absolue :
la norme de la vitesse est conservée. Aucun amortissement ni frottement n'est
appliqué. L'obstacle reste inchangé.

La nouvelle position et la nouvelle vitesse sont enregistrées avec `set_pos`
et `set_velocity`, puis la méthode renvoie `True`.

## 4. Exemple d'utilisation

Depuis la racine du projet :

```python
from physics.hitbox import Hitbox

mobile = Hitbox(x=0, y=0, width=2, height=2)
obstacle = Hitbox(x=6, y=0, width=2, height=10)
mobile.set_velocity(vx=10, vy=0)

collision = mobile.compute_collision(obstacle)

assert collision is True
assert (mobile.x, mobile.y) == (4.0, 0.0)
assert (mobile.vx, mobile.vy) == (-10, 0)
```

Au départ, le bord droit du mobile est à `x = 1` et le bord gauche de
l'obstacle à `x = 5`. La distance à parcourir est donc `4` :

```text
t_entry_x = (5 - 1) / 10 = 0.4
```

Les rectangles se recouvrent déjà sur Y et `vy == 0`, donc cet axe ne limite
pas le contact. Le centre du mobile arrive à `x = 4`, son bord droit touche
l'obstacle à `x = 5`, puis `vx` devient `-10`.

## 5. Intégration dans une simulation et limites

`compute_collision` réalise à la fois la détection et la réponse au contact :

- Si elle renvoie `False`, elle ne modifie ni la position ni la vitesse. Le
  code appelant doit effectuer le déplacement libre lorsque cela convient.
  Attention : `False` peut aussi signifier un chevauchement initial ignoré.
- Si elle renvoie `True`, la position est déjà celle du contact et la vitesse
  est déjà réfléchie. Le temps restant, `1 - t_entry`, n'est pas simulé.

Dans l'exemple, il reste 60 % du pas après le contact. La méthode laisse le
mobile à `x = 4` ; elle ne poursuit pas automatiquement son trajet vers la
gauche. Elle ne renvoie pas non plus `t_entry`, seulement un booléen. Pour
gérer ce temps restant, il faudrait adapter l'interface et prévoir de
nouvelles recherches de collision pendant le reste du pas.

Autres limites de l'implémentation actuelle :

- Seuls des rectangles sans rotation et un obstacle considéré comme fixe sont
  pris en charge. Aucun calcul de vitesse relative entre deux mobiles n'est
  effectué.
- Les chevauchements initiaux ne sont pas résolus : aucun repositionnement
  pour séparer les objets n'est prévu.
- Une seule paire de hitbox est traitée par appel. Avec plusieurs obstacles,
  enchaîner les appels modifie le mobile au fur et à mesure et rend le résultat
  dépendant de l'ordre. Une simulation complète devrait rechercher le contact
  le plus proche avant d'appliquer le rebond.
- Les dimensions ne sont pas validées par le constructeur ; utiliser des
  largeurs et hauteurs strictement positives.
- Trois appels à `print` affichent la position de contact, la nouvelle vitesse
  et les temps d'entrée lorsqu'une collision est détectée.
