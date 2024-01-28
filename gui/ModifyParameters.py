import tkinter as tk
from tkinter import *
from ttkbootstrap import ttk
from ttkbootstrap import Style

class Parameters:
    def __init__(self, object):
        self.root = tk.Tk()

        self.object = object

        # Apply ttkbootstrap theme 'solar'
        self.style = Style(theme='solar')
        self.style.master = self.root

        self.root.title("Parameters")
        self.root.geometry('250x550')
        self.root.resizable(False, False)

        self.parameters_dict = self.object.parameters

        self.theme_choice = tk.StringVar()

        self.create_theme_change_button()

        self.sliders = []
        self.slider_buttons = []

        self.lazer_var = tk.BooleanVar()

        title_label = tk.Label(self.root, text="Enter Parameters:")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        for idx, param in enumerate(self.parameters_dict):
            self.create_element(param, idx+1)

        # Create a button to store parameters
        self.store_button = tk.Button(self.root, text="Store Parameters", command=self.store_parameters)
        self.store_button.grid(row=len(self.parameters_dict) + 3, column=0, columnspan=2, pady=10)

        self.display_initial_values()

        self.root.mainloop()

    def change_theme(self):
        selected_theme = self.theme_choice.get()
        self.style.theme_use(selected_theme)

    def create_theme_change_button(self):
        label_theme = ttk.Label(self.root, text="Select theme:")
        label_theme.grid(row=len(self.parameters_dict) + 4, column=0, columnspan=2, pady=10)

        theme_choices = ["flatly", "darkly", "united", "yeti", "cosmo", "lumen", "sandstone", "superhero", "solar",
                         "cyborg", "vapor", "journal", "litera", "minty", "pulse", "morph", "simplex", "cerculean"]
        theme_combobox = ttk.Combobox(
            self.root, values=theme_choices, state="readonly", textvariable=self.theme_choice
        )
        theme_combobox.grid(row=len(self.parameters_dict) + 5, column=0, columnspan=2, pady=5)

        theme_button = ttk.Button(self.root, text="Change Theme", command=self.change_theme)
        theme_button.grid(row=len(self.parameters_dict) + 6, column=0, columnspan=2, pady=10)

    def create_element(self, param, row):
        label = tk.Label(self.root, text=f"{param.capitalize()}:")
        label.grid(row=row, column=0, padx=5, pady=5, sticky='e')
        if param == 'red' or param == 'blue' or param == 'green':
            slider = tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL, length=150, command=lambda value, param=param: self.update_color_preview(param))
            slider.set(self.parameters_dict[param])
            slider.grid(row=row, column=1, padx=25, pady=5, sticky='w')
            self.sliders.append(slider)

            self.color_preview_canvas = tk.Canvas(self.root, width=50, height=50)
            self.color_preview_canvas.grid(row=len(self.parameters_dict) + 1, column=0, columnspan=2, pady=10)

        elif param == 'lazer':
            checkbutton = ttk.Checkbutton(self.root, style='Roundtoggle.Toolbutton',
                                          variable=self.lazer_var)
            checkbutton.grid(row=row, column=1, padx=25, pady=5, sticky='w')
            self.lazer_var.set(self.parameters_dict[param])
        else:
            entry = ttk.Entry(self.root)
            entry.insert(0, str(self.parameters_dict[param]))  # Set default value
            entry.grid(row=row, column=1, padx=25, pady=5, sticky='w')
            self.parameters_dict[param] = entry  # Store the Entry widget itself, not its value

    def update_color_preview(self, param):
        red = self.sliders[0].get()
        green = self.sliders[1].get()
        blue = self.sliders[2].get()
        color = f'#{int(red):02X}{int(green):02X}{int(blue):02X}'
        self.color_preview_canvas.config(bg=color)


    def store_parameters(self):
        new_parameters = {}

        if len(self.sliders) > 0:
            new_color = []
            for slider in self.sliders:
                color = self.get_slider_value(slider)
                new_color.append(color)
            new_parameters['red'] = new_color[0]
            new_parameters['green'] = new_color[1]
            new_parameters['blue'] = new_color[2]
        if self.lazer_var:
            lazer_on = {'lazer': self.lazer_var.get()}  # Replace this line
            new_parameters.update(lazer_on)


        try:
            for param, entry_widget in self.parameters_dict.items():
                print(param)
                if param == 'lazer' or param == 'red':
                    break
                value = entry_widget.get()
                value = float(value)
                new_parameters[param] = value
            self.object.parameters = new_parameters
        except:
            pass

        self.root.destroy()

    def display_initial_values(self):
        for param, entry_widget in self.parameters_dict.items():
            if isinstance(entry_widget, ttk.Entry):
                value = str(self.parameters_dict[param].get())
                print(f"{param}: {value}")

    def get_slider_value(self, slider):
        return slider.get()


