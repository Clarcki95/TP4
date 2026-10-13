"""
But : Ce fichier contient la classe faisant l'affichage de tkinter et toutes les fonctions qui y sont liées.
Auteur : Tristan GUIEU, Nino BELAOUD
Date : 06/10/26
ToDo : finir Keybinds, affichage du jeu, background du menu principal
"""

import tkinter as tk
from pathlib import Path
from entities.bricks.brick import Brick
from entities.racket import Racket

import numpy as np

from entities.wall import Wall
from entities.ball import Ball

from utils.list import List

L = 1600
H = 1000

TICK_RATE = 100
TICK_DURATION_MS = int(1000 / TICK_RATE)

class Affichage_tkinter(tk.Tk): #fait hérité des propriétés d'une fenêtre tkinter
    def __init__(self):
        super().__init__() #crée la fenêtre

        # Pause
        self.paused = False

        self.title("Casse brique")
        self.geometry("1600x1000")
        self.attributes("-fullscreen", True)

        self.base_canvas = tk.Canvas(self, width = 1600, height = 1000, background="red")
        self.base_canvas.pack(fill="both", expand=True)

        background_path = Path(__file__).resolve().parent.parent / "ressources" / "backgrounds" / "game_bg.gif"
        # Adapter l'image de 1200x750 à la zone de jeu de 1600x1000.
        self.game_background = tk.PhotoImage(file=str(background_path)).zoom(4, 4).subsample(3, 3)
        self.base_canvas.create_image(0, 0, image=self.game_background, anchor=tk.NW)


        self.bind("<Escape>", lambda event: self.toggle_current_menu(self.option_menu))
        self.bind("<Delete>", lambda event : self.close)
        self.bind("<Left>", lambda event : self.Racket.move_left())
        self.bind("<Right>", lambda event : self.Racket.move_right())

        # ================
        # Briques
        #
        self.bricks = List()

        self.bricks.add(Brick(400, 150, self.base_canvas))
        self.bricks.add(Brick(800, 150, self.base_canvas))
        self.bricks.add(Brick(600, 150, self.base_canvas))
        self.bricks.add(Brick(1000, 150, self.base_canvas))
        self.bricks.add(Brick(1200, 150, self.base_canvas))

        # ================

        # ================
        #
        # Balle
        #

        # Vitesse avec angle aléatoire
        v0 = 10
        theta = np.random.uniform(-3 * np.pi/4, -np.pi/2)

        vx = v0 * np.cos(theta)
        vy = v0 * np.sin(theta)

        self.ball = Ball(self.base_canvas, L/2, H/2, vx, vy)
        # ================

        # ================
        #
        # Bordures
        #
        top_wall = Wall(self.base_canvas, L/2, 1, L, 2, True)
        left_wall = Wall(self.base_canvas, 1, H/2, 2, H, True)
        right_wall = Wall(self.base_canvas, L-1, H/2, 2, H, True)
        bottom_wall = Wall(self.base_canvas, L/2, H-1, L, 2, False)

        self.walls = List()
        self.walls.add(top_wall)
        self.walls.add(left_wall)
        self.walls.add(right_wall)
        self.walls.add(bottom_wall)
        # ================

        self.create_option_menu()
        self.create_main_menu()

        self.wm_attributes("-transparentcolor", "yellow") #la couleur jaune devient transparente

    def tick(self):
        # Si on est en pause, on ne met rien à jour
        if self.paused:
            # Relancer le tick
            self.base_canvas.after(TICK_DURATION_MS, self.tick)
            return

        # Tick les collisions
        self.tick_collisions()

        # Mettre à jour la position de la balle
        self.ball.update()

        # Relancer le tick
        self.base_canvas.after(TICK_DURATION_MS, self.tick)

    def tick_collisions(self):
        # Murs
        for wall in self.walls.to_list():
            will_collide = wall.compute_collision(self.ball)
            if will_collide and not wall.is_bouncy():
                # TODO: Fin
                print("Perdu")

        # Briques
        for i, brick in enumerate(self.bricks.to_list()):
            will_collide = brick.compute_collision(self.ball)
            if will_collide:
                # La brique est touchée
                brick.onTouch()

                # Si la brique n'a plus de PV, la supprimer de la liste
                if brick.pv == 0:
                    self.bricks.remove(i)

        self.ball.hitbox.compute_collision(self.Racket.hitbox)

    def toggle_current_menu(self, canva, event=None):
        """
        But : Afficher / Cacher le menu actuel
        Entrée : canva, le menu à afficher ou cacher
        Sortie : aucune
        """
        if canva.winfo_ismapped():
            canva.pack_forget()
            self.paused = False

        elif canva == self.option_menu:
            self.paused = True
            canva.pack(anchor=tk.CENTER, expand=True)

        else:
            canva.pack(fill="both", expand=True)

    def close(self, event):
        """
        But : fermer la fenêtre
        Entrée : (self, classe), (event, évènement tkinter)
        Sortie : aucune
        """
        self.destroy()

    def create_option_menu(self):
        """
        But : créer le menu des options
        Entrée : self, classe
        Sortie : aucune
        """

        #options permettant le calcul automatique des positions des widgets
        Width = 400
        Height = 600
        Outline = 15
        OptionsNumber = 5
        LineOutline = 60

        Space = (Height - 2 * Outline) / (OptionsNumber + 1)

        self.option_menu = tk.Canvas(self.base_canvas, width = Width, height = Height, background="yellow") #création du canva

        #création du style du menu
        self.option_menu.create_rectangle((0, 0), (Height, Height),
                                          outline = "gray",
                                          width = 3,
                                          fill = "white")
        self.option_menu.create_rectangle((Outline, Outline), (Width - Outline, Height - Outline),
                                          outline = "gray",
                                          width = 3,
                                          fill = "black")

        self.option_menu.create_text((Width / 2, Space),
                                     text = "Options",
                                     font = ("Arial", 50),
                                     fill = "white")
        Keybind = self.option_menu.create_text((Width / 2, 2 * Space),
                                     text = "Keybinds",
                                     font = ("Fixedsys", 30),
                                     fill = "white") #on attribue à une varibale pour la lier à une fonction
        BackToMenu = self.option_menu.create_text((Width / 2, 3 * Space),
                                     text = "Back to menu",
                                     font = ("Fixedsys", 30),
                                     fill = "white")
        RestartLevel = self.option_menu.create_text((Width / 2, 4 * Space),
                                     text = "Restart level",
                                     font = ("Fixedsys", 30),
                                     fill = "white")
        Continue = self.option_menu.create_text((Width / 2, 5 * Space),
                                     text = "Continue",
                                     font = ("Fixedsys", 30),
                                     fill = "white")

        self.option_menu.create_line((Outline + LineOutline, (Space + 2 * Space) / 2),
                                     (Width - Outline - LineOutline, (Space + 2 * Space) / 2),
                                     width = 3,
                                     fill = "white")
        self.option_menu.create_line((Outline + LineOutline, (2 * Space + 3 * Space) / 2),
                                     (Width - Outline - LineOutline, (2 * Space + 3 * Space) / 2),
                                     width = 3,
                                     fill = "white")
        self.option_menu.create_line((Outline + LineOutline, (3 * Space + 4 * Space) / 2),
                                     (Width - Outline - LineOutline, (3 * Space + 4 * Space) / 2),
                                     width = 3,
                                     fill = "white")
        self.option_menu.create_line((Outline + LineOutline, (4 * Space + 5 * Space) / 2),
                                     (Width - Outline - LineOutline, (4 * Space + 5 * Space) / 2),
                                     width = 3,
                                     fill = "white")

        #fonctions ajoutant à un évènement une fonction (ici lorsqu'on clique sur le texte, on appelle la fonction)
        self.option_menu.tag_bind(Keybind, "<Button-1>", self.keybinds)
        self.option_menu.tag_bind(BackToMenu, "<Button-1>", self.backToMenu)
        self.option_menu.tag_bind(RestartLevel, "<Button-1>", self.restartLevel)
        self.option_menu.tag_bind(Continue, "<Button-1>", lambda event: self.toggle_current_menu(self.option_menu))

    def create_main_menu(self):
        """
        But : créer le menu principal
        Entrée : self, classe
        Sortie : aucune
        """
        #options permettant le calcul automatique des positions des widgets
        Width = 1600
        Height = 1000
        Outline = Height/6
        OptionsNumber = 5
        LineOutline = Width/3

        Space = (Height - 2 * Outline) / (OptionsNumber + 1)

        self.main_menu = tk.Canvas(self.base_canvas, width = Width, height = Height, background="black") #création du canva

        self.main_menu.create_text((Width / 2, 50 + Space),
                                     text = "Casse Brique",
                                     font = ("Fixedsys", 150),
                                     fill = "green")
        self.main_menu.create_text((Width / 2, Outline + 2 * Space),
                                     text = "Main menu",
                                     font = ("Arial", 70),
                                     fill = "green")
        Start = self.main_menu.create_text((Width / 2, Outline + 3 * Space),
                                     text = "Start",
                                     font = ("Fixedsys", 30),
                                     fill = "green")
        Keybind = self.main_menu.create_text((Width / 2, Outline + 4 * Space),
                                     text = "Keybinds",
                                     font = ("Fixedsys", 30),
                                     fill = "green")
        Exit = self.main_menu.create_text((Width / 2, Outline + 5 * Space),
                                     text = "Exit",
                                     font = ("Fixedsys", 30),
                                     fill = "green")

        self.main_menu.tag_bind(Start, "<Button-1>", self.start)
        self.main_menu.tag_bind(Keybind, "<Button-1>", self.keybinds)
        self.main_menu.tag_bind(Exit, "<Button-1>", self.close)

        self.toggle_current_menu(self.main_menu)

    def start(self, event):
        """
        But : démarrer le jeu
        Entrée : (self, classe), (event, évènement tkinter)
        Sortie : aucune
        """
        self.toggle_current_menu(self.main_menu)

        self.Racket = Racket(self.base_canvas)
        self.base_canvas.tag_raise(self.Racket.rect)
        self.base_canvas.after(TICK_DURATION_MS, self.tick)

    def keybinds(self, event):
        """
        But : permettre l'assignement des touches
        Entrée : (self, classe), (event, évènement tkinter)
        Sortie : (keybinds, tupple)
        """
        Current_canva = None
        if self.option_menu.winfo_ismapped():
            Current_canva = self.option_menu
        else :
            Current_canva = self.main_menu

        self.toggle_current_menu(Current_canva)

    def backToMenu(self, event):
        """
        But : Retourne au menu principal
        Entrée : (self, classe), (event, évènement tkinter)
        Sortie : aucune
        """
        self.toggle_current_menu(self.option_menu)
        self.toggle_current_menu(self.main_menu)

    def restartLevel(self, event):
        """
        But : Recommence le niveau actuel
        Entrée : (self, classe), (event, évènement tkinter)
        Sortie : aucune
        """
        self.toggle_current_menu(self.option_menu)
