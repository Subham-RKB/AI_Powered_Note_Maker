from tkinter import *

def Button_Template(title, description, x1, y1, h, w, commands, frame):
    b1 = Button(frame, text=title+description, font=(
        "bold", 18), bg="black", fg="white", height=h, width=w, command=commands)
    b1.place(x=x1, y=y1)