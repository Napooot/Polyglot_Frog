import os
import psycopg2
from dotenv import load_dotenv, dotenv_values
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

load_dotenv()

@app.route('/')
def home():
    return redirect(url_for('chat')) 

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template('chat.html')

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
                return "Log in successful!"
            else:
                return "Invalid username or password"
        else:
            return "User not found"
        
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

        return render_template('login.html')
    
    return render_template('signup.html') 

if __name__ == "__main__":
    app.run(debug=True)
