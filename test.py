import tkinter
from tkinter import font

root = tkinter.Tk()

def key_handler(event):
    print(event.char, event.keysym, event.keycode)

root.bind("<Key>", key_handler)

popup = tkinter.Menu(root, tearoff=0)
popup.add_command(label="Undo")
popup.add_command(label="Redo")

def show_popup(event):
    popup.post(event.x_root, event.y_root)

root.bind("<Escape>", show_popup)

print(root.winfo_width())

root.mainloop()