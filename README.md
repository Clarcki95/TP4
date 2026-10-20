# TP4

__Auteur:__ **Tristan Guieu**, **Nino BELAOUD**

Jeu de casse-briques en Python avec une interface Tkinter.

## Installation et lancement

Depuis la racine du projet, avec Python 3.10 ou plus et Tkinter disponible :

```powershell
py -m pip install numpy Pillow
py main.py
```

Cliquer sur **Start** pour démarrer. Maintenir les flèches gauche ou droite pour
accélérer la raquette ; elle freine au relâchement et reste dans le canevas.
Le déplacement est calculé à chaque tick. Au rebond, la balle est déviée dans le
sens du déplacement de la raquette, proportionnellement à sa vitesse, sans changer
sa vitesse totale. **Échap** affiche ou masque les options.

Les briques de glace du niveau de test ont une texture bleue et cassent en un coup.
À leur destruction, les frottements de la raquette sont divisés par 5 pendant
5 secondes : elle glisse davantage au relâchement des touches et le fond devient
givré. Casser une autre brique de glace pendant l'effet ne le cumule pas et ne
prolonge pas sa durée. À l'expiration, le fond et les frottements redeviennent
normaux ; une nouvelle brique peut alors déclencher un nouvel effet.

Lorsque toutes les briques cassables ont été détruites, le jeu se met en pause
et affiche **VICTOIRE**, le niveau réussi et le temps de jeu (hors pauses).
Le menu propose **Next level**, **Restart level** et **Back to menu**.
Au dernier niveau, le choix du niveau suivant est désactivé.
Le chronomètre repart à zéro à chaque lancement ou redémarrage d'un niveau.

Les dimensions du jeu, la fréquence de mise à jour et le chemin des ressources
sont regroupés dans `config.py`. Les constantes propres aux entités restent dans
leurs modules.

## Tests

Depuis la racine du projet :

```powershell
.\run_test.bat
```

```powershell
py -m tests.utils.list_test
py -m tests.utils.stack_test
py -m tests.utils.queue_task
py -m tests.physics.hitbox_test
```
