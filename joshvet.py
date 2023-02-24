from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def home():    
    return render_template('home.html.j2')

@app.route('/about')
def about():    
    return render_template('about.html.j2')

@app.route('/links')
def links():    
    return render_template('links.html.j2')
