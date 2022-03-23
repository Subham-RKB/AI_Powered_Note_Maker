from tkinter import *
import templates
import audioPage

##### LANDING PAGE #####
class LandingPage:
    def __init__(self, window):
        self.landingPage = Frame(window)
        self.window = window
        

    def show(self):
        self.landingPage.pack(side = "top", fill = "both", expand = True)
        l1 = Label(self.landingPage, text="MY NOTES", font=(
                "Bernard MT Condensed", 32), bg="#ffffff", fg="black")
        l1.place(x=230, y=30)
        
        templates.Button_Template("+", "", 550, 30, 0, 0, self.AudioUploadPage, self.landingPage)

    def destroy(self):
        self.landingPage.destroy()

    def AudioUploadPage(self):
        pg = audioPage.AudioPage(self.window)
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

# def AudioUploadPage():
#     window.destroy()
#     import audioPage
    
# def LandingPage():
#     l1 = Label(window, text="MY NOTES", font=(
#         "Bernard MT Condensed", 32), bg="#ffffff", fg="black")
#     l1.place(x=230, y=30)
#     Button_Template("+", "", 550, 30, 0, 0, AudioUploadPage)


# def Button_Template(title, description, x1, y1, h, w, commands):
#     b1 = Button(window, text=title+description, font=(
#         "bold", 18), bg="black", fg="white", height=h, width=w, command=commands)
#     b1.place(x=x1, y=y1)


# def convert_to_abstractive():
#     from_audio = """And also, uh, as we discussed about the probability concept, the probability is one of the major concept over here. Randy, so this is basically called as the basic process of conditional probability that probability of a given B, that is the thing which we are trying to identify sometime we might have some additional information. Let's say we have, let's say, apart from the cavity and all, we have something called as weather is sunny, so the traditional information may be relevant, may not be relevant, is not mandatory, that water the information you're catching at a particular point of time because we all are dealing with partially observable system that I already told you in my last class."""
#     #summary = abstractive.summarize(from_audio)
#     # print(summary)


# LandingPage()
# window.mainloop()
