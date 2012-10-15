# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flaskext.lesscss import lesscss


app = Flask(__name__)
app.static_path='/static/'

@app.route('/')
def hello_world():
    return render_template('ayurveda/compatibility.html')

if __name__ == '__main__':
    app.debug = True
    app.run()