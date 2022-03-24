from flask import Flask
from flask import *
import speech_recognition as sr
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
# from string import punctuation
from heapq import nlargest

app = Flask(__name__)

def convertToText(filename):
    r = sr.Recognizer()

    audioFile = sr.AudioFile("./audioFiles/" + filename)

    with audioFile as source:
        audio = r.record(source)

    transcript = r.recognize_google(audio)

    return transcript


def generateKeypoints(text):
    from string import punctuation

    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(text)
    tokens = [token.text for token in doc]
    punctuation = punctuation + '\n'
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text]=1
                else:
                    word_frequencies[word.text]+=1
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores= {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    select_length = int(len(sentence_tokens)*0.3)
    summary = nlargest(select_length,sentence_scores,key= sentence_scores.get)
    final_summary = [word.text for word in summary]
    sentence_cnt = len(final_summary)
    summary = ""
    for idx in range(sentence_cnt):
        summary += str(idx + 1) + ") " + final_summary[idx] + " <br>"
    return summary
    # return final_summary

def generateSummary(transcript):
    text = transcript.split(' ')

    model_name = 'google/pegasus-large'
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)

    result = ""
    textSize = len(text)
    cnt = int(textSize / 300)
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
 
@app.route('/keypoints', methods = ['POST'])
def Keypoints():
    if request.method == 'POST':  
        text = request.form.get("sourceText")

        summary = generateKeypoints(text)

        return summary

 

if __name__ == "__main__":
    app.run()