#Import tkinter library
from tkinter import *
#Create an instance of Tkinter frame or window
win= Tk()
#Set the geometry of tkinter frame
win.geometry("750x250")
#Make the window sticky for every case
win.grid_rowconfigure(0, weight=1)
win.grid_columnconfigure(0, weight=1)
#Create a Label
label=Label(win, text="This is a Centered Text",font=('Aerial 15 bold'))
label.grid(row=2, column=0)

win.mainloop()