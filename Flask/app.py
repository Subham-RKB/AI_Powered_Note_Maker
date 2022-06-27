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

model_name = 'google/pegasus-large'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)

app = Flask(__name__)
chunkCnt = 0

def convertToText(filename):
    r = sr.Recognizer()

    transcript = ""

    for i in range(chunkCnt):

        audioFile = sr.AudioFile("./audio_chunks/" + str(i) + "chunk.wav")

        with audioFile as source:
            audio = r.record(source)

        conversion = r.recognize_google(audio, language="en-IN", show_all=True)
        if(conversion != []):
            transcript += conversion['alternative'][0]['transcript'] + " "
        # print(conversion)
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
    
    # headline = summary[0]
    topWords = nlargest(2, word_frequencies, key= word_frequencies.get)
    headline = ' '.join(topWords)
    print(headline.title())

    res = {}
    res["summary"] = final_summary
    res["headline"] = headline.title()
    # for idx in range(sentence_cnt):
    #     summary += str(idx + 1) + ") " + final_summary[idx] + " \n"
    # return summary
    return res

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

    # model_name = 'google/pegasus-large'
    # tokenizer = PegasusTokenizer.from_pretrained(model_name)
    # model = PegasusForConditionalGeneration.from_pretrained(model_name)

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


# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

def chunkedTranscript(path):
    global chunkCnt
    fullAudio = AudioSegment.from_file(path)
    
    chunks = split_on_silence (
        # Use the loaded audio.
        fullAudio, 
        # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
        min_silence_len = 500,
        # Consider a chunk silent if it's quieter than -16 dBFS.
        # (You may want to adjust this parameter.)
        silence_thresh = fullAudio.dBFS - 16,
        keep_silence= 200
    )

    chunkCnt = len(chunks)

    # Process each chunk with your parameters
    for i, chunk in enumerate(chunks):
        # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
        # silence_chunk = AudioSegment.silent(duration=500)

        # Add the padding chunk to beginning and end of the entire chunk.
        # audio_chunk = silence_chunk + chunk + silence_chunk

        # Normalize the entire chunk.
        # normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

        # Export the audio chunk with new bitrate.
        print("{0}chunk.wav".format(i))
        chunk.export(
            "./audio_chunks/{0}chunk.wav".format(i),
            format = "wav"
        )
    
    # duration = fullAudio.duration_seconds * 1000
    # print(duration)
    # chunkSize = 30000
    # start = 0
    # chunkName = 0
    # while (start < duration):
    #     end = min(duration, start+chunkSize)
    #     chunk = fullAudio[start: end]
    #     start += chunkSize
    #     chunk.export("./audio_chunks/"+str(chunkName) + "chunk.wav", format="wav")
    #     chunkName += 1

    # chunkCnt = chunkName



@app.route('/')
def Landing():
    return render_template('index.html')

@app.route('/summarize', methods = ['POST'])
def Summarize():
    if request.method == 'POST':  
        f = request.files['audioFile'] 
        f.save("./audioFiles/" + f.filename) 
        print(f.filename) 

        chunkedTranscript("./audioFiles/" + f.filename)
        transcript = convertToText(f.filename)

        finalText = structureText(transcript)
        summary = generateSummary(finalText)

        if request.form.get("from") == "recording":
            res = {}
            res["summary"] = summary
            return res
        else:
            return render_template('result.html', summary = summary)
 
@app.route('/keypoints', methods = ['POST'])
def Keypoints():
    if request.method == 'POST':  
        text = request.form.get("sourceText")

        summary = generateKeypoints(text)

        return render_template('keypoints.html', summary = summary["summary"], headline = summary["headline"])

@app.route('/results', methods = ['GET'])
def Results():
    if request.method == 'GET':  
        args = request.args

        return render_template('result.html', summary = args.get("summary"))

 
@app.route('/abstractive', methods = ['POST'])
def Abstractive():
    if request.method == 'POST':  
        text = request.form.get("sourceText")

        summary = generateSummary(text)

        return render_template('result.html', summary = summary)
 

if __name__ == "__main__":
    app.run()