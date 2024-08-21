import tkinter as tk
from tkinter import *
from ttkbootstrap import ttk
from ttkbootstrap import Style
import os
import tkinter.messagebox as messagebox


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
        self.root.grid_columnconfigure(2, weight=1)

        self.style = Style(theme='solar')
        self.style.master = self.root

        self.root.title("Save Game")
        self.root.resizable(False, False)

        title_label = tk.Label(self.root, text="Save game:")
        title_label.grid(row=0, column=0, pady=15, columnspan=3)

        self.entry = ttk.Entry(self.root, justify='center')
        self.entry.grid(row=1, column=0, columnspan=3)

        if self.game.save_title != None:
            self.entry.insert(0, self.game.save_title)

        save_button = tk.Button(self.root, text="Save", command=self.save)
        save_button.grid(row=2, column=0, sticky='e', padx=1, pady=15)

        dont_save_button = tk.Button(self.root, text="Don't Save", command=self.dont_save)
        dont_save_button.grid(row=2, column=1, sticky='n', padx=1, pady=15)

        cancel_save_button = tk.Button(self.root, text="Cancel", command=self.cancel)
        cancel_save_button.grid(row=2, column=2, sticky='w', padx=1, pady=15)

        self.root.geometry(f'250x150')

        self.root.mainloop()

    def dont_save(self):
        """
        Destroys the tkinter window and sets the game's save attribute to False.
        """

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
            save_title = save_title.replace(' ', "_")
            self.old_save_title = self.game.save_title
            self.game.save_title = save_title

            self.dir = "saves"
            self.saves_files = [file[:-5] for file in os.listdir(self.dir) if file.endswith('.json')]

            if self.game.save_title in self.saves_files and self.game.save_title != self.old_save_title:
                messagebox.showerror("Error", "You can not save your game with the same name as another save file.")
            else:
                self.game.save_to_file()
                self.root.destroy()
                self.root.quit()

    def cancel(self):
        self.game.cancel = True
        self.root.destroy()
        self.root.quit()
