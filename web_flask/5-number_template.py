#!/usr/bin/python3
#!/usr/bin/python3
"""
Module: 5-number_template

This script starts a Flask web application.

- Listens on 0.0.0.0, port 5000

Routes:
    '/' - Displays "Hello HBNB!"
    '/hbnb' - Displays "HBNB"
    '/c/<text>' - Displays "C" followed by the value of the text variable,
    '/python/<text>' - Displys "Python" followed by the value of the text
        variable
    '/number/<n> - Displays "n is a number" only if n is an integer
    '/number_template/<n>' - Displays a HTML page only if n is an integer
"""
from flask import Flask, abort, render_template


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


@app.route('/number/<n>', strict_slashes=False)
def n(n):
    """Displays "n is a number" if n is an integer
    otherwise return a 404 error code
    """
    try:
        int(n)
        return f'{n} is a number'
    except ValueError:
        abort(404)


@app.route('/number_template/<n>', strict_slashes=False)
def number_template(n):
    """
    Displays a HTML page if n is an integer
    otherwise return a 404 error code
    """
    try:
        n = int(n)
        return render_template('5-number.html', number=n)
    except ValueError:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
