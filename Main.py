"""Point d'entrée du casse-briques."""

from game.affichage_tkinter import AffichageTkinter


def main() -> None:
    """Crée la fenêtre et lance la boucle d'évènements Tkinter."""
    window = AffichageTkinter()
    window.mainloop()


if __name__ == "__main__":
    main()
