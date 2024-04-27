import pyttsx3
import random
from flask import Flask, request, jsonify, render_template
from responses.default_responses import responses
import openai

app = Flask(__name__)

engine = pyttsx3.init()

openai.api_key = 'sk-proj-9ccWY31eKjTYC0pk4twUT3BlbkFJgyosobGdrEd4qoZ89lLj'  

def text_to_speech(text):
    
    engine.setProperty('rate', 150)   
    engine.setProperty('volume', 0.9)  
    
    voices = engine.getProperty('voices')
    
    female_voice = next((v for v in voices if "female" in v.name.lower()), None)
    if female_voice:
        engine.setProperty('voice', female_voice.id)
    else:
        engine.setProperty('voice', voices[0].id)
 
    engine.say(text)
    engine.runAndWait()

def generate_openai_response(prompt):
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50  
    )

    return response['choices'][0]['text'].strip()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["user_input"].lower()
        
        response = responses.get(user_input)
        
        if response is None:
            response = generate_openai_response(user_input)

        if isinstance(response, list):
            response_text = random.choice(response)
        else:
            response_text = response

        text_to_speech(response_text)

        return jsonify({"response": response_text})

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
