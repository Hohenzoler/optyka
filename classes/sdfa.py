import tkinter as tk
from tkinter import ttk

def on_select(event):
    selected_item = dropdown.get()
    print("Selected item:", selected_item)

# Create a Tkinter window
window = tk.Tk()
window.title("Dropdown Menu Example")

# Create a Combobox widget
dropdown = ttk.Combobox(window, values=["Option 1", "Option 2", "Option 3"])

# Set default value
dropdown.set("Select an option")

# Bind the event handler to the dropdown menu
dropdown.bind("<<ComboboxSelected>>", on_select)

# Place the dropdown menu in the window
dropdown.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()
