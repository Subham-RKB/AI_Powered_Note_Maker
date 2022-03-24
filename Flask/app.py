from flask import Flask
from flask import *
import speech_recognition as sr
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch

app = Flask(__name__)

def convertToText(filename):
    r = sr.Recognizer()

    audioFile = sr.AudioFile("./audioFiles/" + filename)

    with audioFile as source:
        audio = r.record(source)

    transcript = r.recognize_google(audio)

    return transcript


def generateSummary(transcript):
    text = transcript.split(' ')

    model_name = 'google/pegasus-large'
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)

    result = ""
    textSize = len(text)
    cnt = int(textSize / 200)
    for i in range(cnt + 1):
        j = i*100
        cur = ""

        while(j < min((i+1) * 100, textSize)):
            cur += text[j] + ' '
            j += 1

        tokens = tokenizer(cur, truncation=True, padding="longest", return_tensors="pt")
        summary = model.generate(**tokens)
        summarized_text = tokenizer.decode(summary[0])
        result += summarized_text + ' '

    return result



@app.route('/')
def Landing():
    return render_template('index.html')

@app.route('/summarize', methods = ['POST'])
def Summarize():
    if request.method == 'POST':  
        f = request.files['audioFile']  
        f.save("./audioFiles/" + f.filename)  

        transcript = convertToText(f.filename)

        summary = generateSummary(transcript)

        return summary

        

if __name__ == "__main__":
    app.run()