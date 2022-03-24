from flask import Flask

app = Flask(__name__)

@app.route('/')
def Landing():
    return "Landing Page"

@app.route('/transcribe')
def Trancsribe():
    return "Transcribing"

@app.route('/summarize')
def Summarize():
    return "Summarizing"

if __name__ == "__main__":
    app.run()