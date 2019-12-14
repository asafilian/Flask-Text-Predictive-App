from flask import render_template, request
from predictivetext import application
import re
import string
from sqlalchemy import *
import pandas as pd
from predictivetext.prediction import get_next_backoff, preprocess_str

@application.route("/", methods=['GET', 'POST'])
@application.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form['text']
        suggestions = get_next_backoff(text)
        first = ''
        if text != '':
            first = text + ' ' + suggestions[0]
        return render_template('home.html', text = text, first=first,  suggestions=suggestions)
    else:
        return render_template('home.html', suggestions='')


@application.route("/about")
def about():
    return render_template("about.html", title='About')
