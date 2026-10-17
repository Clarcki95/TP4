
import tkinter as tk

class Main_menu(tk.Canvas):
    def __init__(self, canva, width, height, start, keybinds, close):
        super().__init__(canva, width = width, height = height, background = "black")

        self.width = width
        self.height = height
        self.outline = height / 6
        self.options_number = 5
        self.space = (height - 2 * self.outline) / (self.options_number + 1)

        self.start = start
        self.keybinds = keybinds
        self.close = close

        self.create_menu()

    def create_menu(self):
        self.create_text(
            (self.width / 2, 50 + self.space),
            text="Casse Brique",
            font=("Fixedsys", 150),
            fill="green",
        )
        self.create_text(
            (self.width / 2, self.outline + 2 * self.space),
            text="Main menu",
            font=("Arial", 70),
            fill="green",
        )
        start_button = self.create_text(
            (self.width / 2, self.outline + 3 * self.space),
            text="Start",
            font=("Fixedsys", 30),
            fill="green",
        )
        keybind = self.create_text(
            (self.width / 2, self.outline + 4 * self.space),
            text="Keybinds",
            font=("Fixedsys", 30),
            fill="green",
        )
        exit_button = self.create_text(
            (self.width / 2, self.outline + 5 * self.space),
            text="Exit",
            font=("Fixedsys", 30),
            fill="green",
        )

        self.tag_bind(start_button, "<Button-1>", self.start)
        self.tag_bind(keybind, "<Button-1>", lambda event : self.keybinds(None, event))
        self.tag_bind(exit_button, "<Button-1>", self.close)
        self.toggle_visibility()

    def is_visible(self):
        return self.winfo_ismapped()

    def toggle_visibility(self, trash = None):
        if self.is_visible() :
            self.pack_forget()
        else :
            self.pack(fill="both", expand=True)