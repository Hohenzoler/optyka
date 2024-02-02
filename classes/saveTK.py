import tkinter as tk
from tkinter import *
from ttkbootstrap import ttk
from ttkbootstrap import Style

class Save:
    """
    A class to represent the save functionality of a game.

    ...

    Attributes
    ----------
    root : Tk
        a toplevel widget of Tk which represents the main window of an application
    game : obj
        the game object that is being saved
    style : Style
        the style object for the tkinter window
    entry : Entry
        the entry widget used to get the save title from the user

    Methods
    -------
    dont_save():
        Destroys the tkinter window and sets the game's save attribute to False.
    save():
        Gets the save title from the entry widget, replaces spaces with underscores,
        sets the game's save attribute to True and the game's save_title attribute to the save title,
        and then destroys the tkinter window.
    """

    def __init__(self, game):
        """
        Constructs all the necessary attributes for the save object.

        Parameters
        ----------
            game : obj
                the game object that is being saved
        """

        self.root = tk.Tk()
        self.game = game

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.style = Style(theme='solar')
        self.style.master = self.root

        self.root.title("Save Game")
        self.root.resizable(False, False)

        title_label = tk.Label(self.root, text="Save game:")
        title_label.grid(row=0, column=0, pady=15, columnspan=2)

        self.entry = ttk.Entry(self.root, justify='center')
        self.entry.grid(row=1, column=0, columnspan=2)

        save_button = tk.Button(self.root, text="Save", command=self.save)
        save_button.grid(row=2, column=0, sticky='e', padx=10, pady=15)

        cancel_button = tk.Button(self.root, text="Don't Save", command=self.dont_save)
        cancel_button.grid(row=2, column=1, sticky='w', padx=10, pady=15)

        self.root.geometry(f'250x150')

        self.root.mainloop()

    def dont_save(self):
        """
        Destroys the tkinter window and sets the game's save attribute to False.
        """

        self.game.save = False

        self.root.destroy()
        self.root.quit()

    def save(self):
        """
        Gets the save title from the entry widget, replaces spaces with underscores,
        sets the game's save attribute to True and the game's save_title attribute to the save title,
        and then destroys the tkinter window.
        """

        save_title = self.entry.get().strip()

        if save_title != '':

            self.game.save = True
            save_title = save_title.replace(' ', "_")
            self.game.save_title = save_title

            self.root.destroy()
            self.root.quit()
