"""
But : Ce fichier contient la classe faisant l'affichage de tkinter et toutes les fonctions qui y sont liées.
Auteur : Tristan GUIEU
Date : 06/10/26
ToDo : finir Keybinds, affichage du jeu, background du menu principal
"""

import tkinter as tk

class Affichage_tkinter(tk.Tk): #fait hérité des propriétés d'une fenêtre tkinter
    def __init__(self):
        super().__init__() #crée la fenêtre

        self.title("Casse brique")
        self.geometry("1600x1000")

        self.bind("<Escape>", lambda event: self.toggle_current_menu(self.option_menu))
        self.bind("<Delete>", self.close)

        self.create_option_menu()
        self.create_main_menu()

        self.wm_attributes("-transparentcolor", "yellow") #la couleur jaune devient transparente

    def toggle_current_menu(self, canva, event=None):
        """
        But : Afficher / Cacher le menu actuel
        Entrée : (self, classe), (event, évènement tkinter)
        Sortie : aucune
        """
        if canva.winfo_ismapped() :
            canva.pack_forget() #cache le canva
        elif canva == self.main_menu :
            self.main_menu.pack(fill="both", expand=True) #rend le canva visible, fill l'écran et s'étend
        else :
            canva.pack(anchor=tk.CENTER, expand=True) #permet de placer le canva au centre, expansible
    
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

        self.option_menu = tk.Canvas(self, width = Width, height = Height, background="yellow") #création du canva

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

        self.main_menu = tk.Canvas(self, width = Width, height = Height, background="black") #création du canva

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