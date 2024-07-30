#!/usr/bin/python3
"""
Module: 3-python_route

This script starts a Flask web application.

- Listens on 0.0.0.0, port 5000

Routes:
    '/' - Displays "Hello HBNB!"
    '/hbnb' - Displays "HBNB"
    '/c/<text>' - Displays "C" followed by the value of the text variable,
    '/python/<text>' - Displys "Python" followed by the value of the text
        variable
"""
from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Display 'Hello HBNB!' """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Display 'HBNB' """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """ Display 'C' followed by the value of the text variable
    with underscore replaced by spaces
    """
    return f"C {text.replace('_', ' ')}"


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text):
    """Display 'Python' followed by the value of the text variable
    with underscores replaced by spaces and default set to "is cool"
    """
    return f"Python {text.replace('_', ' ')}"


if __name__ == '__main__':
    app.run(debug=True)
