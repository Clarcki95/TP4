"""

"""

import tkinter as tk
import physics.hitbox as hitbox

SPEED = 20
WIDTH = 150
HEIGHT = 30


class Racket() :
    def __init__(self, canva: tk.Canvas):
        self.hitbox = hitbox.Hitbox(50, 800, WIDTH, HEIGHT)
        self.canva = canva
        self.create()

    def create(self):
        width = self.canva.winfo_width()
        height = self.canva.winfo_height()

        racket_width = WIDTH
        racket_height = HEIGHT
        bottom_margin = 100

        self.rect = self.canva.create_rectangle(
            width / 2 - racket_width / 2,
            height - bottom_margin - racket_height,
            width / 2 + racket_width / 2,
            height - bottom_margin,
            fill="white"
        )

    def move_left(self):
        if 0 < self.canva.coords(self.rect)[0] :
            self.canva.move(self.rect, -SPEED, 0)
            self.hitbox.set_pos(self.canva.coords(self.rect)[0] + WIDTH/2, self.canva.coords(self.rect)[1] + HEIGHT/2)

    def move_right(self):
        if self.canva.coords(self.rect)[0] + WIDTH < self.canva.winfo_width() :
            self.canva.move(self.rect, SPEED, 0)
            self.hitbox.set_pos(self.canva.coords(self.rect)[0] + WIDTH/2, self.canva.coords(self.rect)[1] + HEIGHT/2)
