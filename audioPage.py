from tkinter import *
from tkinter import filedialog
import speech_recognition as sr
import abstractive

from templates import Button_Template
import landingPage

##### AUDIO PAGE #####
class AudioPage:
    def __init__(self, window):
        self.audioPage = Frame(window)
        self.window = window
        self.fileTitle = ""
        
    def show(self):
        self.audioPage.pack(side = "top", fill = "both", expand = True)
        l1 = Label(self.audioPage, text="Upload Audio", font=(
                "Bernard MT Condensed", 30), bg="#ffffff", fg="black")
        l1.place(x=230, y=30)

        Button_Template("Back","",4,4,1,4,self.LandingPage,self.audioPage)

        Button_Template("Upload","",200,100,1,5,self.uploadAudio,self.audioPage)

        self.l3 = Label(self.audioPage, text=self.fileTitle, font=("Lora", 12), bg="#ffffff", fg="black")
        

    def uploadAudio(self):
        self.filePath = filedialog.askopenfilename(initialdir="/audioFiles", title="Select a File", filetypes = (("wav files", "*.wav"), ("All files", "*.*")))

        self.fileTitle = self.filePath.split('/')[-1]
        
        self.l3["text"] = self.fileTitle
        self.l3.place_forget()
        self.l3.place(x=200, y=200)

        Button_Template("Summarize","",200,150,1,10,self.Summarize,self.audioPage)

    def Summarize(self):
        r = sr.Recognizer()

        self.l3["text"] = "Fetching Audio File ..."
        self.l3.place_forget()
        self.l3.place(x=200, y=200)

        audioFile = sr.AudioFile(self.filePath)

        with audioFile as source:
            audio = r.record(source)

        self.l3["text"] = "Transcribing Audio ..."
        self.l3.place_forget()
        self.l3.place(x=200, y=200)

        transcript = r.recognize_google(audio)

        self.l3["text"] = "Summarizing ..."
        self.l3.place_forget()
        self.l3.place(x=200, y=200)

        summary = abstractive.summarize(transcript)

        print(summary)


        

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
