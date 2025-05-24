import os
import psycopg2
from dotenv import load_dotenv, dotenv_values
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

load_dotenv()
# Connect to the database
conn = psycopg2.connect(database=os.getenv("MY_DATABASE"),
                        user=os.getenv("USER"),
                        password=os.getenv("PASSWORD"),
                        host=os.getenv("HOST"),
                        port=os.getenv("PORT"))

# Create a cursor (used to retrieve, manipulate, and process data from db)
cur = conn.cursor()

# .excute means query, .commit means commit
# remember to always close the cursor and connection when finished

# Test to add a user
cur.execute(
    # "INSERT INTO users (username, email, passhash) VALUES (%s, %s, %s);",
    # ("Napooot", "test@gmail.com", "bobisthecoolest123")
    # "DELETE FROM users WHERE username = %s;", ("Napooot",)
)

conn.commit()
cur.close()
conn.close()