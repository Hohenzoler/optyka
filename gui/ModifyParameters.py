import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap import ttk

class Parameters:
    def __init__(self, object):
        self.root = tk.Tk()

        self.object = object

        # Apply ttkbootstrap theme 'solar'
        self.style = Style(theme='solar')
        self.style.master = self.root

        self.root.title("Parameters")
        self.root.geometry('250x450')
        self.root.resizable(False, False)

        self.parameters_dict = self.object.parameters

        self.sliders = []

        title_label = tk.Label(self.root, text="Enter Parameters:")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        for idx, param in enumerate(self.parameters_dict):
            self.create_element(param, idx+1)

        # Create a button to store parameters
        self.store_button = tk.Button(self.root, text="Store Parameters", command=self.store_parameters)
        self.store_button.grid(row=len(self.parameters_dict) + 3, column=0, columnspan=2, pady=10)

        self.display_initial_values()

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

        try:
            for param, entry_widget in self.parameters_dict.items():
                if param == 'red':
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