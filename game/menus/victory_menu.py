"""Menu affiché lorsqu'un niveau est terminé."""

import tkinter as tk


class Victory_menu(tk.Canvas):
    def __init__(self, canva, next_level, restart_level, back_to_menu):
        self.width = 400
        self.height = 600
        self.outline = 15
        self.options_number = 5
        self.line_outline = 60
        self.space = (self.height - 2 * self.outline) / (self.options_number + 1)
        super().__init__(
            canva, width=self.width, height=self.height,
            background="yellow",
        )

        self.next_level = next_level
        self.restart_level = restart_level
        self.back_to_menu = back_to_menu

        self.create_menu()

    def create_menu(self):
        self.create_rectangle(
            (0, 0), (self.width, self.height),
            outline="gray", width=3, fill="white",
        )
        self.create_rectangle(
            (self.outline, self.outline),
            (self.width - self.outline, self.height - self.outline),
            outline="gray", width=3, fill="black",
        )
        self.create_text(
            self.width / 2, self.space, text="VICTOIRE",
            font=("Fixedsys", 42), fill="green",
        )
        self.level_text = self.create_text(
            self.width / 2, 1.8 * self.space, font=("Fixedsys", 22), fill="white",
            width=self.width - 60, justify=tk.CENTER,
        )
        self.time_text = self.create_text(
            self.width / 2, 2.3 * self.space,
            font=("Fixedsys", 22), fill="white",
        )
        next_level = self.create_text(
            self.width / 2, 3 * self.space, text="Next level",
            font=("Fixedsys", 26), fill="white", tags=("next_level",),
        )
        restart_level = self.create_text(
            self.width / 2, 4 * self.space, text="Restart level",
            font=("Fixedsys", 26), fill="white",
        )
        back_to_menu = self.create_text(
            self.width / 2, 5 * self.space, text="Back to menu",
            font=("Fixedsys", 26), fill="white", justify=tk.CENTER,
        )
        for index in range(2, self.options_number):
            separator_y = (index + 0.5) * self.space
            self.create_line(
                self.outline + self.line_outline, separator_y,
                self.width - self.outline - self.line_outline, separator_y,
                fill="white", width=3,
            )
        self.tag_bind(next_level, "<Button-1>", self.next_level)
        self.tag_bind(restart_level, "<Button-1>", self.restart_level)
        self.tag_bind(back_to_menu, "<Button-1>", self.back_to_menu)

    def is_visible(self):
        return self.winfo_ismapped()

    def show(self, level_name: str, has_next_level: bool, elapsed_seconds: float) -> None:
        """Affiche le résultat et désactive la progression au dernier niveau."""
        self.itemconfigure(self.level_text, text=f"{level_name} réussi !")
        minutes, seconds = divmod(int(elapsed_seconds), 60)
        self.itemconfigure(self.time_text, text=f"Temps : {minutes:02d}:{seconds:02d}")
        self.itemconfigure(
            "next_level",
            state=tk.NORMAL if has_next_level else tk.DISABLED,
            fill="white" if has_next_level else "gray",
            disabledfill="gray",
        )
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        tk.Misc.tkraise(self)
