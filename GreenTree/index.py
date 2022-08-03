from config import *
from flask import render_template

@app.route('/')
@app.route('/index/')
def index():
    languages = ["C++", "Python", "PHP", "Java", "C", "Ruby",
                     "R", "C#", "Dart", "Fortran", "Pascal", "Javascript"]
    return render_template('index.html', languages=languages)