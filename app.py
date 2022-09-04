
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.htm")

@app.route("/login")
def login():
    return render_template("login.htm")

