from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
import pyodbc

app = Flask(__name__)

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')