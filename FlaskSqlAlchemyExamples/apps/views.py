from flask import render_template

from apps import app


@app.route('/')
def hello_world():
    return render_template("index.html")
