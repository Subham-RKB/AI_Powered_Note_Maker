from tkinter import *

from templates import Button_Template
import landingPage

##### AUDIO PAGE #####
class AudioPage:
    def __init__(self, window):
        self.audioPage = Frame(window)
        self.window = window
        

    def show(self):
        self.audioPage.pack(side = "top", fill = "both", expand = True)
        l1 = Label(self.audioPage, text="MY Audios", font=(
                "Bernard MT Condensed", 32), bg="#ffffff", fg="black")
        l1.place(x=230, y=30)
        Button_Template("Back","",200,250,2,30,self.LandingPage,self.audioPage)

    def destroy(self):
        self.audioPage.destroy()
    def LandingPage(self):
        pg = landingPage.LandingPage(self.window)
        pg.show()
        self.destroy()










# import os
# from tkinter import *
# from tkinter import messagebox
# #import abstractive
# # creating the application main window
# window = Tk()
# window.title("AI Powered Note Maker")
# window.geometry("600x600")
# window.configure(bg="#ffffff")
# currentPage = "landing"
# def nextPage():
#     window.destroy()
#     import landingPage

# def Button_Template(title, description, x1, y1, h, w, commands):
#     b1 = Button(window, text=title+description, font=(
#         "bold", 18), bg="black", fg="white", height=h, width=w, command=commands)
#     b1.place(x=x1, y=y1)


# def AudioUploadPage():
#     Button_Template("Done", "", 10, 10, 2, 45,nextPage)

# AudioUploadPage()
# window.mainloop()
