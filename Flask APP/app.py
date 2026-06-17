from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("secret_key")

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')