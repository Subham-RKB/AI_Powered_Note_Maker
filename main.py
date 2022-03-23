import os
from tkinter import *
from tkinter import messagebox
import landingPage
import audioPage
#import abstractive
# creating the application main window
window = Tk()
window.title("AI Powered Note Maker")
window.geometry("600x600")
window.configure(bg="#ffffff")

pg1 = landingPage.LandingPage(window)
pg2 = audioPage.AudioPage(window)

pg1.show()



# def LandingPage():
#     l1 = Label(window, text="MY NOTES", font=(
#         "Bernard MT Condensed", 32), bg="#ffffff", fg="black")
#     l1.place(x=230, y=30)
#     Button_Template("+", "", 550, 30, 0, 0,AudioUploadPage, landingPage)



# def Button_Template(title, description, x1, y1, h, w, commands, frame):
#     b1 = Button(frame, text=title+description, font=(
#         "bold", 18), bg="black", fg="white", height=h, width=w, command=commands)
#     b1.place(x=x1, y=y1)


def convert_to_abstractive():
    from_audio = """And also, uh, as we discussed about the probability concept, the probability is one of the major concept over here. Randy, so this is basically called as the basic process of conditional probability that probability of a given B, that is the thing which we are trying to identify sometime we might have some additional information. Let's say we have, let's say, apart from the cavity and all, we have something called as weather is sunny, so the traditional information may be relevant, may not be relevant, is not mandatory, that water the information you're catching at a particular point of time because we all are dealing with partially observable system that I already told you in my last class."""
    #summary = abstractive.summarize(from_audio)
    # print(summary)



# def rough():
#     global currentPage
#     currentPage = "landing"
#     LandingPage()

# def AudioUploadPage():
#     global currentPage
#     currentPage = "audio"
#     Button_Template("Done", "", 10, 10, 2, 45,rough, audioPage)

# pageMap = {
#     "landing" : landingPage,
#     "audio" : audioPage
# }

# def clearFrame():
#     global window
#     for widget in window.winfo_children():
#        widget.place_forget()

# def ChangePage(page):
#     # global window
#     # global currentPage
#     # clearFrame()
#     pageMap[page].tkraise()

# if currentPage == "landing":
#     ChangePage("landing")
#     # LandingPage()
#     # for i in range(1, 10):
#     #     Button_Template("Chaps", "\nHe is a good Boy.", 13, 100*i+5, 2, 40,rough())

# elif currentPage == "audio":
#     ChangePage("audio")
#     # AudioUploadPage()


window.mainloop()
