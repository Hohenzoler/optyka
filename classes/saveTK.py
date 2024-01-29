import tkinter as tk
from tkinter import *
from ttkbootstrap import ttk
from ttkbootstrap import Style

class Save:
    def __init__(self, game):
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
        self.game.save = False

        self.root.destroy()
        self.root.quit()

    def save(self):

        save_title = self.entry.get().strip()

        if save_title != '':

            self.game.save = True
            save_title = save_title.replace(' ', "_")
            self.game.save_title = save_title

            self.root.destroy()
            self.root.quit()
# a = Save()