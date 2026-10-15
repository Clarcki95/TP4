"""
But : Affichage Tkinter, menus et boucle de mise à jour du jeu.
Auteur : Tristan GUIEU, Nino BELAOUD
Date : 06/10/26
TODO : finir les raccourcis clavier, l'affichage du jeu et le fond du menu principal.
"""

import tkinter as tk

import numpy as np

from config import GAME_HEIGHT, GAME_WIDTH, RESOURCES_DIR, TICK_DURATION_MS
from entities.ball import Ball
from entities.bricks.brick import Brick
from entities.racket import Racket
from entities.wall import Wall
from utils.list import List
from game.menus.option_menu import Option_menu
from game.menus.main_menu import Main_menu


class AffichageTkinter(tk.Tk):
    """Fenêtre principale regroupant le jeu et ses menus."""

    def __init__(self) -> None:
        super().__init__()
        self.paused = False
        self.pressed_keys = set()

        self.configure_window()
        self.bind_controls()

        self.main_menu = Main_menu(self.base_canvas, 
                                     GAME_WIDTH, 
                                     GAME_HEIGHT, 
                                     self.start, 
                                     self.keybinds, 
                                     self.close)
        
        self.option_menu = Option_menu(self.base_canvas, 
                                       self.keybinds, 
                                       self.back_to_menu, 
                                       self.restart_level,
                                       self.tick_pause)

        # Le jaune sert de couleur transparente aux menus.
        self.wm_attributes("-transparentcolor", "yellow")

    def configure_window(self) -> None:
        """Configure la fenêtre et crée le canevas du jeu."""
        self.title("Casse brique")
        self.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}")
        self.attributes("-fullscreen", True)

        self.base_canvas = tk.Canvas(
            self, width=GAME_WIDTH, height=GAME_HEIGHT, background="red"
        )
        self.base_canvas.pack(fill="both", expand=True)

    def create_background(self) -> None:
        """Charge et dimensionne l'image de fond du jeu."""
        background_path = RESOURCES_DIR / "backgrounds" / "game_bg.gif"
        # Adapter l'image de 1200x750 à la zone de jeu de 1600x1000.
        self.game_background = (
            tk.PhotoImage(file=str(background_path)).zoom(4, 4).subsample(3, 3)
        )
        self.base_canvas.create_image(
            0, 0, image=self.game_background, anchor=tk.NW
        )

    def bind_controls(self) -> None:
        """Associe les touches aux actions du jeu."""
        self.bind(
            "<Escape>", lambda event: self.option_menu.toggle_visibility()
        )
        self.bind("<Delete>", lambda event: self.close)

        # Movement
        self.bind("<KeyPress-Left>", self.press_movement_key)
        self.bind("<KeyRelease-Left>", self.release_movement_key)
        self.bind("<KeyPress-Right>", self.press_movement_key)
        self.bind("<KeyRelease-Right>", self.release_movement_key)

    def press_movement_key(self, event: tk.Event) -> None:
        """Mémorise une flèche maintenue sans déplacer la raquette."""
        if not self.paused:
            self.pressed_keys.add(event.keysym)

    def release_movement_key(self, event: tk.Event) -> None:
        """Oublie la flèche relâchée, même pendant la pause."""
        self.pressed_keys.discard(event.keysym)

    def reset_movement(self, event=None) -> None:
        """Évite les touches bloquées après une pause ou une perte de focus."""
        self.pressed_keys.clear()

    def create_bricks(self) -> None:
        """Crée les cinq briques du niveau."""
        self.bricks = List()
        for pos_x in (400, 800, 600, 1000, 1200):
            self.bricks.add(Brick(pos_x, 150, self.base_canvas))

    def create_ball(self) -> None:
        """Crée la balle avec sa vitesse et son angle de départ aléatoire."""
        v0 = 10
        theta = np.random.uniform(-3 * np.pi / 4, -np.pi / 2)
        vx = v0 * np.cos(theta)
        vy = v0 * np.sin(theta)
        self.ball = Ball(
            self.base_canvas, GAME_WIDTH / 2, GAME_HEIGHT / 2, vx, vy
        )

    def create_walls(self) -> None:
        """Crée les murs dans l'ordre haut, gauche, droite, bas."""
        top_wall = Wall(self.base_canvas, GAME_WIDTH / 2, 1, GAME_WIDTH, 2, True)
        left_wall = Wall(self.base_canvas, 1, GAME_HEIGHT / 2, 2, GAME_HEIGHT, True)
        right_wall = Wall(self.base_canvas, GAME_WIDTH - 1, GAME_HEIGHT / 2, 2, GAME_HEIGHT, True)
        bottom_wall = Wall(self.base_canvas, GAME_WIDTH / 2, GAME_HEIGHT - 1, GAME_WIDTH, 2, False)

        self.walls = List()
        self.walls.add(top_wall)
        self.walls.add(left_wall)
        self.walls.add(right_wall)
        self.walls.add(bottom_wall)

    def tick(self) -> None:
        """Met à jour le jeu puis programme la prochaine itération."""
        if self.paused:
            self.tick_id = self.base_canvas.after(TICK_DURATION_MS, self.tick)
            return

        # Mettre à jour la raquette avant de tester les collisions.
        direction = int("Right" in self.pressed_keys) - int("Left" in self.pressed_keys)
        self.racket.update(direction)

        # Tick les collisions
        self.tick_collisions()

        # Mettre à jour la position de la balle
        self.ball.update()

        # Relancer le tick
        self.tick_id = self.base_canvas.after(TICK_DURATION_MS, self.tick)

    def tick_collisions(self) -> None:
        """Traite les collisions avec les murs, les briques et la raquette."""
        for wall in self.walls.to_list():
            will_collide = wall.compute_collision(self.ball)
            if will_collide and not wall.is_bouncy():
                # TODO : gérer la fin de partie.
                print("Perdu")

        for index, brick in enumerate(self.bricks.to_list()):
            will_collide = brick.compute_collision(self.ball)
            if will_collide:
                brick.on_touch()
                if brick.pv == 0:
                    self.bricks.remove(index)

        self.racket.compute_collision(self.ball)

    def tick_pause(self, state) -> None:
        self.paused = state

    def toggle_current_menu(self, canvas: tk.Canvas, event=None) -> None:
        """Bascule la visibilité du menu et active la pause pour les options."""
        self.reset_movement()
        if canvas.winfo_ismapped():
            canvas.pack_forget()
            self.tick_pause(False)
        else:
            canvas.pack(fill="both", expand=True)

    def close(self, event: tk.Event) -> None:
        """Ferme la fenêtre du jeu."""
        self.destroy()

    def start(self, event: tk.Event) -> None:
        """Masque le menu principal, crée la raquette et lance les ticks."""
        self.main_menu.toggle_visibility()

        self.create_background()
        self.create_ball()
        self.create_walls()
        self.create_bricks()

        self.racket = Racket(self.base_canvas)
        self.base_canvas.tag_raise(self.racket.rect)
        self.tick_id = self.base_canvas.after(TICK_DURATION_MS, self.tick)

    def stop(self) -> None:
        """Arrête les ticks et détruit la balle, bricks, walls et raquette."""
        self.reset_movement()
        self.base_canvas.after_cancel(self.tick_id)
        self.base_canvas.delete('all')

        for brick in self.bricks.to_list():
            brick.destroy()

        self.walls = List()
        self.bricks = List()
        self.tick_id = ""

    def keybinds(self, event: tk.Event) -> None:
        """Masque le menu courant en attendant l'écran des raccourcis."""
        # TODO : permettre l'assignation des touches.
        if self.option_menu.winfo_ismapped():
            current_canvas = self.option_menu
        else:
            current_canvas = self.main_menu
        self.toggle_current_menu(current_canvas)

    def back_to_menu(self, event: tk.Event) -> None:
        """Bascule des options vers le menu principal."""
        self.stop()
        self.option_menu.toggle_visibility()
        self.main_menu.toggle_visibility()

    def restart_level(self, event: tk.Event) -> None:
        """Bascule la visibilité du menu des options."""
        # TODO : réinitialiser le niveau.
        self.option_menu.toggle_visibility()
