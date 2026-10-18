
import tkinter as tk

class Gameover_menu(tk.Canvas):
    def __init__(self, canva, back_to_menu, restart_game, exit):
        self.width = 400
        self.height = 600

        super().__init__(canva, width = self.width, height = self.height, background = "yellow")

        self.back_to_menu = back_to_menu
        self.restart_game = restart_game
        self.exit = exit

        self.width = 400
        self.height = 600
        self.outline = 15
        self.options_number = 5
        self.line_outline = 60
        self.space = (self.height - 2 * self.outline) / (self.options_number + 1)

        self.create_menu()

    def create_menu(self):
        self.create_rectangle(
            (0, 0), (self.height, self.height), outline="gray", width=3, fill="white"
        )

        self.create_rectangle(
            (self.outline, self.outline),
            (self.width - self.outline, self.height - self.outline),
            outline="gray",
            width=3,
            fill="black",
        )

        self.create_text(
            (self.width / 2, self.space),
            text="GAME",
            font=("Fixedsys", 50),
            fill="red",
        )

        keybind = self.create_text(
            (self.width / 2, 2 * self.space),
            text="OVER",
            font=("Fixedsys", 50),
            fill="red",
        )

        back_to_menu = self.create_text(
            (self.width / 2, 3 * self.space),
            text="Back to menu",
            font=("Fixedsys", 30),
            fill="white",
        )

        restart_game = self.create_text(
            (self.width / 2, 4 * self.space),
            text="Restart game",
            font=("Fixedsys", 30),
            fill="white",
        )

        exit = self.create_text(
            (self.width / 2, 5 * self.space),
            text="Exit",
            font=("Fixedsys", 30),
            fill="white",
        )

        for index in range(2, self.options_number):
            separator_y = (index * self.space + (index + 1) * self.space) / 2
            self.create_line(
                (self.outline + self.line_outline, separator_y),
                (self.width - self.outline - self.line_outline, separator_y),
                width=3,
                fill="white",
            )

        self.tag_bind(back_to_menu, "<Button-1>", self.back_to_menu)
        self.tag_bind(restart_game, "<Button-1>", self.restart_game)
        self.tag_bind(exit, "<Button-1>", self.exit,
        )   

    def is_visible(self):
        return self.winfo_ismapped()

    def toggle_visibility(self):
        if self.is_visible():
            self.place_forget()
        else:
            self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            tk.Misc.tkraise(self)