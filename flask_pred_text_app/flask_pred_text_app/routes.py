from flask import render_template, request
from flask_pred_text_app import app
from flask_pred_text_app.prediction import get_next_backoff

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
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

    # sug_str = ''
    # if request.method == 'POST':
    #     text = request.form['text']
    #     suggestions = prediction.get_next_backoff(text)
    #     if suggestions != '':
    #         for i, item in enumerate(suggestions):
    #             sug_str = sug_str + '  [' + format(i+1) + '] ' + item
    #     return render_template('home.html', suggested=sug_str)
    # else:
    #     return render_template('home.html', suggested=sug_str)

@app.route("/about")
def about():
    return render_template("about.html", title='About')
