from flask import Flask
from flask import *
import os
import speech_recognition as sr
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
# from string import punctuation
from heapq import nlargest
from pydub import AudioSegment
from pydub.silence import split_on_silence

app = Flask(__name__)
chunkCnt = 0

def convertToText(filename):
    r = sr.Recognizer()

    transcript = ""

    for i in range(chunkCnt):

        audioFile = sr.AudioFile("./audio_chunks/" + str(i) + "chunk.wav")

        with audioFile as source:
            audio = r.record(source)

        conversion = r.recognize_google(audio)
        transcript += conversion + " "

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
    # for idx in range(sentence_cnt):
    #     summary += str(idx + 1) + ") " + final_summary[idx] + " \n"
    # return summary
    return final_summary

def structureText(transcript):
    text = transcript.split()

    result = ""
    textSize = len(text)
    cnt = int(textSize / 20)
    for i in range(cnt + 1):
        j = i*20
        cur = ""

        while(j < min((i+1) * 20, textSize)):
            cur += text[j] + ' '
            j += 1
        result += cur + ". "
    return result    


def generateSummary(transcript):
    text = transcript.strip().split(". ")

    model_name = 'google/pegasus-large'
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)

    result = ""
    textSize = len(text)
    cnt = int(textSize / 6)
    for i in range(cnt + 1):
        j = i*6
        cur = ""

        while(j < min((i+1) * 6, textSize)):
            cur += text[j] + ". "
            j += 1

        tokens = tokenizer(cur, truncation=True, padding="longest", return_tensors="pt")
        
        summary_ids = model.generate(tokens["input_ids"])
        summarized_text = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

        # summary = model.generate(**tokens)
        # summarized_text = tokenizer.decode(summary[0])
        result += summarized_text + ' '

    return result


def chunkedTranscript(path):
    global chunkCnt
    fullAudio = AudioSegment.from_wav(path)
    duration = fullAudio.duration_seconds * 1000
    print(duration)
    chunkSize = 30000
    start = 0
    chunkName = 0
    while (start < duration):
        end = min(duration, start+chunkSize)
        chunk = fullAudio[start: end]
        start += chunkSize
        chunk.export("./audio_chunks/"+str(chunkName) + "chunk.wav", format="wav")
        chunkName += 1

    chunkCnt = chunkName



@app.route('/')
def Landing():
    return render_template('index.html')

@app.route('/summarize', methods = ['POST'])
def Summarize():
    if request.method == 'POST':  
        f = request.files['audioFile'] 
        if(f.filename[-3:] != "wav"):
            f.filename += ".wav" 
        f.save("./audioFiles/" + f.filename) 
        print(f.filename) 

        chunkedTranscript("./audioFiles/" + f.filename)
        transcript = convertToText(f.filename)

        finalText = structureText(transcript)
        summary = generateSummary(finalText)

        return render_template('result.html', summary = summary)
 
@app.route('/keypoints', methods = ['POST'])
def Keypoints():
    if request.method == 'POST':  
        text = request.form.get("sourceText")

        summary = generateKeypoints(text)

        return render_template('keypoints.html', summary = summary)

 
@app.route('/abstractive', methods = ['POST'])
def Abstractive():
    if request.method == 'POST':  
        text = request.form.get("sourceText")

        summary = generateSummary(text)

        return render_template('result.html', summary = summary)
 

if __name__ == "__main__":
    app.run()