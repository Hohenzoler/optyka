import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttk
import os

class Parameters:
    def __init__(self, object):
        self.root = ttk.Window(themename='solar')

        self.root.protocol('WM_DELETE_WINDOW', self.passed)

        self.object = object

        # # Apply ttkbootstrap theme 'solar'
        # self.style = Style()
        # self.style.master = self.root

        self.root.title("Parameters")
        self.root.resizable(False, False)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.parameters_dict = self.object.parameters

        self.points = self.object.points

        self.TextureDropdown = None

        self.sliders = []
        self.slider_buttons = []

        title_label = tk.Label(self.root, text="Enter Parameters:")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        for idx, param in enumerate(self.parameters_dict):
            self.create_element(param, idx+1)

        # Create a button to store parameters
        self.store_button = tk.Button(self.root, text="Store Parameters", command=self.store_parameters)
        self.store_button.grid(row=len(self.parameters_dict) + 3, column=0, columnspan=2, pady=10)

        self.root.geometry(f'300x{60*len(self.parameters_dict)}')

        self.root.mainloop()

    def create_element(self, param, row):
        try:
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
                self.slider_buttons.append(ToggleSwitch(self.parameters_dict[param], self.root))
                self.slider_buttons[0].grid(row=row, column=1, padx=25, pady=5, sticky='w')

            elif param == 'texture':
                self.textureOptions = [file[:-4].capitalize() for file in os.listdir("images/materials") if file.endswith('.png')]
                self.TextureDropdown = ttk.Combobox(self.root, values=self.textureOptions)
                self.TextureDropdown.grid(row=row, column=1, padx=25, pady=5, sticky='w')
                self.TextureDropdown.set(self.parameters_dict[param].capitalize())

            else:
                try:
                    entry = tk.Entry(self.root)
                    if param != 'size':
                        if param in ['reflection_factor', 'transmittance']:
                            entry.insert(0, f'{str(self.parameters_dict[param] * 100)}%')  # Set default value in percentage
                        else:
                            entry.insert(0, str(self.parameters_dict[param])) # Set default value
                    else:
                        entry.insert(0, f'{str(self.parameters_dict[param] * 100)}%')# Set default value
                    entry.grid(row=row, column=1, padx=25, pady=5, sticky='w')
                    self.parameters_dict[param] = entry  # Store the Entry widget itself, not its value
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

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

        if len(self.slider_buttons) > 0:
            lazer_on = {'lazer': self.slider_buttons[0].value}
            new_parameters.update(lazer_on)

        if self.TextureDropdown != None:
            new_parameters['texture'] = self.TextureDropdown.get().lower()

        try:
            for param, entry_widget in self.parameters_dict.items():
                if param == 'lazer' or param == 'red' or param == 'texture':
                    break
                value = entry_widget.get()

                if param == 'size':
                    value = str(value)
                    value = value.strip("%")
                    value = float(value) / 100
                    # self.object.points = self.change_size(value)

                if param == 'reflection_factor' or param == 'transmittance':
                    value = str(value)
                    value = value.strip("%")
                    value = float(value) / 100
                    if value < 0:
                        value = 0
                    elif value > 1:
                        value = 1
                    new_parameters[param] = value

                value = float(value)
                new_parameters[param] = value

            if new_parameters.get('reflection_factor') + new_parameters.get('transmittance') > 1:
                messagebox.showerror("Error", "The sum of reflection factor and transmittance cannot exceed 100%.")
                return

            print(new_parameters)
            self.object.parameters.update(new_parameters)
        except Exception as e:
            print(e)

        self.root.quit()
        self.root.destroy()

    def get_slider_value(self, slider):
        return slider.get()

    def passed(self):
        pass



class ToggleSwitch(tk.Canvas):
    def __init__(self, value, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=60, height=30, bd=0, highlightthickness=0)
        self.value = value
        self.create_rounded_rectangle()
        self.bind("<Button-1>", self.toggle)

    def create_rounded_rectangle(self):
        radius = 10

        rgb_color_blue = (7, 54, 66)
        hex_color_blue = "#{:02x}{:02x}{:02x}".format(*rgb_color_blue)

        rgb_color_outline = (11, 81, 98)
        hex_color_outline = "#{:02x}{:02x}{:02x}".format(*rgb_color_outline)

        self.create_oval(5, 25 - 2 * radius, 5 + 2 * radius, 25, fill=hex_color_blue, outline=hex_color_outline)
        self.create_oval(45 - 2 * radius, 25 - 2 * radius, 55, 25, fill=hex_color_blue, outline=hex_color_outline)
        self.create_rectangle(5 + radius, 5, 55 - radius, 25, fill=hex_color_blue, outline=hex_color_outline)
        self.create_rectangle(5 + radius, 7, 55 - radius, 23, fill=hex_color_blue, outline=hex_color_blue)

        # self.create_oval(2, 2, 28, 28, fill=hex_color_gold, outline="black", width=2, tags="slider")
        self.update_oval_color()

    def toggle(self, event):
        self.value = not self.value
        self.update_oval_color()

    def update_oval_color(self):
        try:
            self.delete("slider")
        except:
            pass
        amount_to_move = 0
        if self.value:
            rgb_color = (188, 149, 26)
            amount_to_move = 30
        else:
            rgb_color = (169, 169, 169)

        hex_color = "#{:02x}{:02x}{:02x}".format(*rgb_color)

        self.create_oval(2, 2, 28, 28, fill=hex_color, outline="black", width=2, tags="slider")

        self.move("slider", amount_to_move, 0)
class TestObj:
    def __init__(self):
        self.parameters = {'x': 100, 'y': 250, 'angle': 90, 'lazer': False, 'red': 198, 'green': 23, 'blue': 103}

