# Import SpeechRecognition Library

import speech_recognition as sr
from tkinter import filedialog

r = sr.Recognizer()

fname = filedialog.askopenfilename(initialdir="/audioFiles", title="Select a File", filetypes = (("wav files", "*.wav"), ("All files", "*.*")))

audioFile = sr.AudioFile("./audioFiles/test1.wav")

with audioFile as source:
    audio = r.record(source)

transcript = r.recognize_google(audio)

print(transcript)




