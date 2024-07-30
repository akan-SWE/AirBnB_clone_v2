#!/usr/bin/python3
"""
Module: 0-hello_route

This script starts a Flask web application.

- Listens on 0.0.0.0, port 5000

Routes:
    '/' - Displays "Hello HBNB!"
    '/hbnb' - Displays "HBNB"
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return 'HBNB'


if __name__ == '__main__':
    app.run(debug=True)
