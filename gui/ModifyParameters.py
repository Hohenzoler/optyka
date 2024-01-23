import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap import ttk

class Parameters:
    def __init__(self, object):
        self.root = tk.Tk()

        # Apply ttkbootstrap theme 'solar'
        style = Style(theme='solar')
        style.master = self.root

        self.root.title("Parameters")
        self.root.geometry('250x300')
        self.root.resizable(False, False)

        self.parameters_dict = object.parameters

        title_label = tk.Label(self.root, text="Enter Parameters:")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        for idx, param in enumerate(self.parameters_dict):
            self.create_entry(param, idx+1)

        # Create a button to store parameters
        self.store_button = tk.Button(self.root, text="Store Parameters", command=self.store_parameters)
        self.store_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.display_initial_values()

        self.root.mainloop()

    def create_entry(self, param, row):
        label = tk.Label(self.root, text=f"{param.capitalize()}:")
        label.grid(row=row, column=0, padx=5, pady=5, sticky='e')

        entry = ttk.Entry(self.root)
        entry.insert(0, str(self.parameters_dict[param]))  # Set default value
        entry.grid(row=row, column=1, padx=25, pady=5, sticky='w')
        self.parameters_dict[param] = entry  # Store the Entry widget itself, not its value

    def store_parameters(self):
        for param, entry_widget in self.parameters_dict.items():
            value = entry_widget.get()
            print(f"{param}: {value}")

    def display_initial_values(self):
        for param, entry_widget in self.parameters_dict.items():
            if isinstance(entry_widget, ttk.Entry):
                value = str(self.parameters_dict[param].get())
                print(f"{param}: {value}")

if __name__ == "__main__":
    parameters_dict = {'x': 23, 'y': 342, 'width': 23, 'height': 4, 'angle': 32}
    window = Parameters(parameters_dict)
