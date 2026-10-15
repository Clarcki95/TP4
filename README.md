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

Les dimensions du jeu, la fréquence de mise à jour et le chemin des ressources
sont regroupés dans `config.py`. Les constantes propres aux entités restent dans
leurs modules.

## Tests

Depuis la racine du projet :

```powershell
.\run_test.bat
```

Les cinq suites peuvent également être exécutées séparément :

```powershell
py -m tests.utils.list_test
py -m tests.utils.stack_test
py -m tests.utils.queue_task
py -m tests.physics.hitbox_test
py -m tests.racket_test
```
