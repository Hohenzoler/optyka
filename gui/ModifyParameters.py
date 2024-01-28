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

        self.points = self.object.points

        self.sliders = []
        self.slider_buttons = []

        title_label = tk.Label(self.root, text="Enter Parameters:")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        for idx, param in enumerate(self.parameters_dict):
            self.create_element(param, idx+1)

        # Create a button to store parameters
        self.store_button = tk.Button(self.root, text="Store Parameters", command=self.store_parameters)
        self.store_button.grid(row=len(self.parameters_dict) + 3, column=0, columnspan=2, pady=10)


        self.root.mainloop()

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
            try:
                self.var_lazer = tk.BooleanVar(value=self.parameters_dict[param])
                self.slider_buttons.append(ttk.Checkbutton(self.root, offvalue=False, onvalue=True, variable=self.var_lazer))
                self.slider_buttons[0].grid(row=row, column=1, padx=25, pady=5, sticky='w')
            except Exception as e:
                print(e)


        else:
            try:
                entry = ttk.Entry(self.root)
                if param != 'size':
                    entry.insert(0, str(self.parameters_dict[param]))# Set default value
                else:
                    entry.insert(0, f'{str(self.parameters_dict[param] * 100)}%')# Set default value
                entry.grid(row=row, column=1, padx=25, pady=5, sticky='w')
                self.parameters_dict[param] = entry  # Store the Entry widget itself, not its value
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

            lazer_on = {'lazer': self.var_lazer.get()}
            new_parameters.update(lazer_on)


        try:
            for param, entry_widget in self.parameters_dict.items():
                if param == 'lazer' or param == 'red':
                    break

                value = entry_widget.get()

                if param == 'size':
                    value = str(value)
                    print(value)
                    value = value.strip("%")
                    value = float(value)/100
                    self.object.points = self.change_size(value)

                value = float(value)
                new_parameters[param] = value

            self.object.parameters.update(new_parameters)
        except Exception as e:
            print(e)

        self.root.quit()
        self.root.destroy()

    def get_slider_value(self, slider):
        return slider.get()


    def change_size(self, percent):

        new_points = []

        for point in self.points:
            new_x = ((point[0] - float(self.parameters_dict['x'].get())) * percent) + float(self.parameters_dict['x'].get())
            new_y = (point[1] - float(self.parameters_dict['y'].get())) * percent + float(self.parameters_dict['y'].get())

            new_points.append((new_x, new_y))
        return new_points

class TestObj:
    def __init__(self):
        self.parameters = {'x': 100, 'y': 250, 'angle': 90, 'lazer': False, 'red': 198, 'green': 23, 'blue': 103}

