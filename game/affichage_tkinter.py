"""
But : Affichage Tkinter, menus et boucle de mise à jour du jeu.
Auteur : Tristan GUIEU, Nino BELAOUD
Date : 06/10/26
TODO : l'affichage du jeu et le fond du menu principal.
"""

import tkinter as tk
from time import monotonic

import numpy as np

from config import (
    ASSIGNED_KEYS,
    GAME_HEIGHT,
    GAME_WIDTH,
    RESOURCES_DIR,
    TICK_DURATION_MS,
)
from entities.ball import Ball
from entities.racket import Racket
from entities.wall import Wall
from game.levels.level_manager import LevelManager
from game.menus.gameover_menu import Gameover_menu
from game.menus.keybinds_menu import Keybinds_menu
from game.menus.main_menu import Main_menu
from game.menus.option_menu import Option_menu
from game.menus.victory_menu import Victory_menu
from sound.sound_manager import Sound_manager
from utils.list import List


class AffichageTkinter(tk.Tk):
    """Fenêtre principale regroupant le jeu et ses menus."""

    def __init__(self) -> None:
        super().__init__()
        self.paused = False
        self.game_on = False
        self.level_won = False
        self.level_elapsed_time = 0.0
        self.level_timer_started_at = None
        self.waiting_for_key = False
        self.pressed_keys = set()
        self.tick_id = None
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.assigned_keys = ASSIGNED_KEYS
        self.previous_assigned_keys = self.assigned_keys.copy()
        self.sound_manager = Sound_manager()

        self.sound_manager = Sound_manager()

        self.configure_window()
        self.bind_controls()
        self.create_menus()

        # Préparer les niveaux
        self.setup_level_manager()

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
        self.ice_background = (
            tk.PhotoImage(file=str(RESOURCES_DIR / "backgrounds" / "game_bg_ice.png"))
            .zoom(4, 4).subsample(3, 3)
        )
        self.background_drawing = self.base_canvas.create_image(
            0, 0, image=self.game_background, anchor=tk.NW
        )
        self.background_frozen = False

    def freeze_racket(self) -> None:
        """Active la glissade et affiche immédiatement le fond givré."""
        self.racket.freeze()
        self.update_ice_background()

    def update_ice_background(self) -> None:
        """Synchronise le fond avec l'effet de glace de la raquette."""
        frozen = self.racket.ice_started_at is not None
        if frozen != self.background_frozen:
            self.base_canvas.itemconfig(
                self.background_drawing,
                image=self.ice_background if frozen else self.game_background,
            )
            self.background_frozen = frozen

    def create_menus(self) -> None:
        """Crée les menus et associe leurs boutons aux actions de la fenêtre."""
        self.keybinds_menu = Keybinds_menu(
            self.base_canvas,
            self.assigned_keys,
            self.change_key,
            self.changing_waiting_for_key,
        )
        self.main_menu = Main_menu(
            self.base_canvas,
            GAME_WIDTH,
            GAME_HEIGHT,
            self.start,
            self.keybinds,
            self.close,
        )
        self.option_menu = Option_menu(
            self.base_canvas,
            self.keybinds,
            self.back_to_menu,
            self.restart_level,
            self.tick_pause,
        )
        self.gameover_menu = Gameover_menu(
            self.base_canvas,
            self.back_to_menu,
            self.restart_level,
            self.close,
        )
        self.victory_menu = Victory_menu(
            self.base_canvas, self.next_level, self.restart_level, self.back_to_menu
        )

    def bind_controls(self) -> None:
        """Associe les touches aux actions du jeu."""
        self.bind(
            f"<{self.assigned_keys['toggle_menu']}>",
            lambda event: self.choose_menu_toggling(),
        )
        self.bind(f"<{self.assigned_keys['exit_game']}>", lambda event: self.close())

        # Movement
        self.bind(f"<KeyPress-{self.assigned_keys['left']}>", self.press_movement_key)
        self.bind(
            f"<KeyRelease-{self.assigned_keys['left']}>", self.release_movement_key
        )
        self.bind(f"<KeyPress-{self.assigned_keys['right']}>", self.press_movement_key)
        self.bind(
            f"<KeyRelease-{self.assigned_keys['right']}>", self.release_movement_key
        )

    def update_binds(self):
        for key in self.previous_assigned_keys.values():
            for sequence in (
                f"<{key}>",
                f"<KeyPress-{key}>",
                f"<KeyRelease-{key}>",
            ):
                self.unbind(sequence)

        self.previous_assigned_keys = self.assigned_keys.copy()
        self.bind_controls()

    def change_key(self, assigned_key_dico):
        self.assigned_keys = assigned_key_dico
        self.update_binds()

    def press_movement_key(self, event: tk.Event) -> None:
        """Mémorise une flèche maintenue sans déplacer la raquette."""
        if not self.paused:
            self.pressed_keys.add(event.keysym)

    def release_movement_key(self, event: tk.Event) -> None:
        """Oublie la flèche relâchée, même pendant la pause."""
        self.pressed_keys.discard(event.keysym)

    def choose_menu_toggling(self):
        if self.waiting_for_key:
            return

        if self.victory_menu.is_visible():
            return

        if self.keybinds_menu.is_visible():
            self.keybinds_menu.toggle_visibility()

        elif self.option_menu.is_visible():
            self.option_menu.toggle_visibility()

        elif self.gameover_menu.is_visible():
            self.gameover_menu.toggle_visibility()

        elif self.main_menu.is_visible():
            self.main_menu.toggle_visibility()

        elif self.game_on:
            self.option_menu.toggle_visibility()

        else:
            self.main_menu.toggle_visibility()

    def reset_movement(self, event=None) -> None:
        """Évite les touches bloquées après une pause ou une perte de focus."""
        self.pressed_keys.clear()

    def setup_level_manager(self) -> None:
        """Initialise les définitions des niveaux pour le canevas du jeu."""
        self.level_manager = LevelManager(
            self.base_canvas, self.sound_manager, self.freeze_racket
        )

    def create_ball(self) -> None:
        """Crée la balle avec sa vitesse et son angle de départ aléatoire."""
        v0 = 10
        theta = np.random.uniform(-3 * np.pi / 4, -np.pi / 2)
        vx = v0 * np.cos(theta)
        vy = v0 * np.sin(theta)
        self.ball = Ball(self.base_canvas, GAME_WIDTH / 2, GAME_HEIGHT / 2, vx, vy)

    def create_walls(self) -> None:
        """Crée les murs dans l'ordre haut, gauche, droite, bas."""
        top_wall = Wall(self.base_canvas, GAME_WIDTH / 2, 1, GAME_WIDTH, 2, True)
        left_wall = Wall(self.base_canvas, 1, GAME_HEIGHT / 2, 2, GAME_HEIGHT, True)
        right_wall = Wall(
            self.base_canvas, GAME_WIDTH - 1, GAME_HEIGHT / 2, 2, GAME_HEIGHT, True
        )
        bottom_wall = Wall(
            self.base_canvas, GAME_WIDTH / 2, GAME_HEIGHT - 1, GAME_WIDTH, 2, False
        )

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
        direction = int(self.assigned_keys["right"] in self.pressed_keys) - int(
            self.assigned_keys["left"] in self.pressed_keys
        )
        self.racket.update(direction)

        # Tick les collisions
        self.tick_collisions()
        self.update_ice_background()

        if not self.paused:
            # Verifier la victoire
            self.check_win_condition()

        # Mettre à jour la balle seulement si le niveau continue.
        if not self.paused:
            self.ball.update()

        self.tick_id = self.base_canvas.after(TICK_DURATION_MS, self.tick)

    def check_win_condition(self) -> None:
        """Détecte la victoire quand il ne reste aucune brique cassable."""
        if not self.game_on or self.level_won:
            return

        if any(brick.pv > 0 for brick in self.level_manager.get_bricks().to_list()):
            return

        self.level_won = True
        self.tick_pause(True)
        self.reset_movement()
        self.victory_menu.show(
            self.level_manager.get_selected_level().get_level_name(),
            self.level_manager.has_next_level(),
            self.level_elapsed_time,
        )

    def tick_collisions(self) -> None:
        """Traite les collisions avec les murs, les briques et la raquette."""
        # Collisions avec les murs
        for wall in self.walls.to_list():
            will_collide = wall.compute_collision(self.ball)
            if will_collide and not wall.is_bouncy():
                self.game_over()
                return
            if will_collide:
                self.sound_manager.sound("bounce")

        level_manager = self.level_manager
        bricks = level_manager.get_bricks().to_list()

        # Collisions avec les briques
        destroyed_indices = []
        for index, brick in enumerate(bricks):
            will_collide = brick.compute_collision(self.ball)
            if will_collide:
                brick.on_touch()
                self.sound_manager.sound("death" if brick.pv == 0 else "bounce")
                if brick.pv == 0:
                    destroyed_indices.append(index)

        # Retirer depuis la fin pour conserver les indices des autres briques
        for index in reversed(destroyed_indices):
            level_manager.remove_brick(index)

        is_racket_collision = self.racket.compute_collision(self.ball)

        if is_racket_collision:
            self.sound_manager.sound("bounce_racket")

    def tick_pause(self, state) -> None:
        """Suspend ou reprend le jeu en excluant les pauses du chronomètre."""
        now = monotonic()
        if self.level_timer_started_at is not None:
            self.level_elapsed_time += now - self.level_timer_started_at
        self.level_timer_started_at = (
            now if not state and self.game_on and not self.level_won else None
        )
        self.paused = state

    def changing_waiting_for_key(self, new_state):
        self.waiting_for_key = new_state

    def game_over(self):
        self.tick_pause(True)
        self.game_on = False
        self.reset_movement()
        self.gameover_menu.toggle_visibility()
        self.sound_manager.sound("defeat")

    def next_level(self, event: tk.Event | None = None) -> None:
        """Nettoie le terrain et démarre le niveau suivant s'il existe."""
        if not self.level_won or not self.level_manager.has_next_level():
            return

        self.stop()
        self.level_manager.select_level(self.level_manager.selected_level_id + 1)
        self.start()

    def close(self, event: tk.Event | None = None) -> None:
        """Arrête la boucle principale pour fermer proprement le jeu."""
        if self.waiting_for_key:
            return

        if self.tick_id:
            try:
                self.after_cancel(self.tick_id)
            except tk.TclError:
                pass
            self.tick_id = None

        self.sound_manager.close()
        self.quit()

    def start(self, event: tk.Event | None = None) -> None:
        """Démarre une partie après le nettoyage de la précédente avec stop()."""
        # Masquer explicitement les menus.
        self.main_menu.place_forget()
        self.option_menu.place_forget()
        self.gameover_menu.place_forget()
        self.keybinds_menu.place_forget()
        self.victory_menu.place_forget()

        self.reset_movement()
        self.paused = False
        self.game_on = True
        self.level_won = False

        self.create_background()
        self.create_ball()
        self.create_walls()
        # Instancier de nouvelles briques sans réutiliser les widgets détruits.
        self.level_manager.init_level()

        self.racket = Racket(self.base_canvas, self.sound_manager)
        self.base_canvas.tag_raise(self.racket.rect)

        self.level_elapsed_time = 0.0
        self.level_timer_started_at = monotonic()
        self.tick_id = self.base_canvas.after(TICK_DURATION_MS, self.tick)

    def stop(self) -> None:
        """Arrête les ticks et détruit les éléments du jeu."""

        self.tick_pause(True)
        self.game_on = False
        self.reset_movement()

        if self.tick_id:
            try:
                self.base_canvas.after_cancel(self.tick_id)
            except tk.TclError:
                pass

            self.tick_id = None

        # delete() efface les dessins du canevas, mais pas les widgets enfants.
        self.base_canvas.delete("all")

        self.walls = List()
        # Les briques sont des labels : les détruire séparément des dessins.
        self.level_manager.clear_level()

    def keybinds(self, last_menu, event: tk.Event) -> None:
        """Masque le menu courant en attendant l'écran des raccourcis."""
        # TODO : permettre l'assignation des touches.
        self.keybinds_menu.toggle_visibility(last_menu)

    def back_to_menu(self, event: tk.Event | None = None) -> None:
        """Nettoie la partie et affiche uniquement le menu principal."""
        self.stop()
        self.option_menu.place_forget()
        self.gameover_menu.place_forget()
        self.keybinds_menu.place_forget()
        self.victory_menu.place_forget()
        if not self.main_menu.is_visible():
            self.main_menu.toggle_visibility()

        # Remet le niveau à 0
        self.level_manager.select_level(0)

    def restart_level(self, event: tk.Event | None = None) -> None:
        """Nettoie la partie actuelle puis en démarre une nouvelle."""
        # Annuler le tick et détruire les anciens éléments avant de les recréer.
        self.stop()
        self.start()
