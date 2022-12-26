from flask import Flask, render_template, url_for
from datetime import date



app = Flask(__name__)

@app.template_filter()
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

@app.route('/')
def home():
    return render_template('index.html.j2')

@app.route('/pets')
def pets():
    return render_template('pets.html.j2')