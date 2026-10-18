
import tkinter as tk

class Keybinds_menu(tk.Canvas):
    def __init__(self, canva, assigned_keys, change_key, changing_waiting_for_key):
        self.width = 400
        self.height = 600

        super().__init__(canva, width = self.width, height = self.height, background = "yellow")

        self.assigned_keys = assigned_keys
        self.change_key = change_key
        self.changing_waiting_for_key = changing_waiting_for_key
        self.waiting_for_key = None
        
        self.width = 400
        self.height = 600
        self.outline = 15
        self.options_number = 6
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
            text="Keybinds",
            font=("Arial", 50),
            fill="white",
        )

        toggle_menu = self.create_text(
            (self.width / 2, 2 * self.space),
            text="Toggle menu " + self.assigned_keys["toggle_menu"],
            font=("Fixedsys", 20),
            fill="white",
        )

        exit_game = self.create_text(
            (self.width / 2, 3 * self.space),
            text="Exit game " + self.assigned_keys["exit_game"],
            font=("Fixedsys", 20),
            fill="white",
        )

        left = self.create_text(
            (self.width / 2, 4 * self.space),
            text="Left " + self.assigned_keys["left"],
            font=("Fixedsys", 20),
            fill="white",
        )

        right = self.create_text(
            (self.width / 2, 5 * self.space),
            text="Right " + self.assigned_keys["right"],
            font=("Fixedsys", 20),
            fill="white",
        )

        continue_button = self.create_text(
            (self.width / 2, 6 * self.space),
            text="Continue",
            font=("Fixedsys", 30),
            fill="white",
        )

        for index in range(1, self.options_number):
            separator_y = (index * self.space + (index + 1) * self.space) / 2
            self.create_line(
                (self.outline + self.line_outline, separator_y),
                (self.width - self.outline - self.line_outline, separator_y),
                width=3,
                fill="white",
            )

        self.tag_bind(
            toggle_menu,
            "<Button-1>",
            lambda event: self.get_key("toggle_menu")
        )

        self.tag_bind(
            exit_game,
            "<Button-1>",
            lambda event: self.get_key("exit_game")
        )

        self.tag_bind(
            left,
            "<Button-1>",
            lambda event: self.get_key("left")
        )

        self.tag_bind(
            right,
            "<Button-1>",
            lambda event: self.get_key("right")
        )

        self.tag_bind(
            continue_button,
            "<Button-1>",
            lambda event: self.toggle_visibility(),
        )

    def get_key(self, key):
        """Attend que l'utilisateur appuie sur une nouvelle touche."""
        self.waiting_for_key = key
        self.changing_waiting_for_key(True)

        # Attend la prochaine touche pressée sur la fenêtre principale.
        self.winfo_toplevel().bind(
            "<KeyPress>",
            self.on_key_pressed
        )


    def on_key_pressed(self, event):
        """Enregistre la touche pressée."""

        if self.waiting_for_key is None:
            return

        key = self.waiting_for_key

        # Convertit la touche en nom exploitable par Tkinter.
        new_key = event.keysym

        self.assigned_keys[key] = new_key

        # Informe la classe principale du changement.
        self.change_key(self.assigned_keys)
        self.waiting_for_key = None
        self.changing_waiting_for_key(False)

        # Retire la capture temporaire du clavier.
        self.winfo_toplevel().unbind("<KeyPress>")

        # Actualise l'affichage du menu.
        self.delete("all")
        self.create_menu()

    def is_visible(self):
        return self.winfo_ismapped()

    def toggle_visibility(self, last_menu=None):
        if self.is_visible():
            self.pack_forget()

            if self.last_menu != None:
                self.last_menu.toggle_visibility()

        else:
            self.last_menu = last_menu

            if self.last_menu != None:
                self.last_menu.toggle_visibility(False)

            self.pack(anchor=tk.CENTER, expand=True)
            tk.Misc.tkraise(self)