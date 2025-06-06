import os
import psycopg2
import io
import base64
from dotenv import load_dotenv, dotenv_values
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from openai import OpenAI


app = Flask(__name__)
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_AI_KEY").strip())
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/')
def home():
    return redirect(url_for('chat')) 

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template('chat.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    file = request.files["audio"]
    buffer = io.BytesIO(file.read())
    buffer.name = "audio.webm"

    response = client.audio.transcriptions.create(
        model='whisper-1',
        file=buffer
    )

    return {"output": response.text}

@app.route('/output_backend', methods=['POST'])
def output_backend():
    data = request.json
    userInput = data.get("input")
    
    # Get text response from OpenAI
    input = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly, multilingual assistant. Your task is to have a conversation with the user and correct any mistakes they make while speaking. They are new to the language and are learning. Maintain a friendly tone that is open to teaching."},
            {"role": "user", "content": userInput}
        ]
    )

    # Processing for TTS
    textOutput = input.choices[0].message.content

    tts = client.audio.speech.create(
        model="tts-1",
        voice="shimmer",
        input=textOutput
    )

    # Convert the audio content to base64 for frontend usage
    audio = base64.b64encode(tts.content).decode('utf-8')
    return jsonify({
        "output": textOutput,
        "audio": audio
    })


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        passwordRaw = request.form.get('password')

        conn = psycopg2.connect(
            database=os.getenv("MY_DATABASE"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT")
        )
        cur = conn.cursor()

        cur.execute(
            "SELECT passhash FROM users WHERE username = %s;", (username,)
        )
        # fetches exactly one row from my SQL query
        result = cur.fetchone()

        cur.close()
        conn.close()

        if result:
            storedHash = result[0]

            # Check if the raw password matches the hash
            if check_password_hash(storedHash, passwordRaw):
                flash('You were successfully logged in')
                return redirect(url_for('chat')) 
            else:
                flash('Invalid username or password. Please try again.')
                return redirect(url_for('login')) 
        else:
            flash("User not found")
            return redirect(url_for('signup')) 
        
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get data from the form
        username = request.form.get('username')
        email = request.form.get('email')
        passwordRaw = request.form.get('password')

        # Hash the password to secure it
        password = generate_password_hash(passwordRaw)

        # Connect to the database
        conn = psycopg2.connect(
            database=os.getenv("MY_DATABASE"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT")
        )
        cur = conn.cursor()

        # Insert the new user
        cur.execute(
            "INSERT INTO users (username, email, passhash) VALUES (%s, %s, %s);",
            (username, email, password)
        )

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('login')) 
    
    return render_template('signup.html') 

if __name__ == "__main__":
    app.run(debug=True)
