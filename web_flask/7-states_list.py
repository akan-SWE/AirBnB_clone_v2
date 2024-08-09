#!/usr/bin/python3
"""
Module: 7-states_list

Flask web application

Routes:
    '/states_list' - Displays a HTML page containing all States objects

Function:
    clean_session: Remove the current session after each request
"""

from models.model_registry import mapped_classes
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def clean_session(exception):
    """
    Remove the current session after each request.
    """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Display an HTML page that lists all States objects in ascending order
    by name.
    """
    state_list = list(storage.all(mapped_classes['State']).values())
    states_sorted = sorted(state_list, key=lambda s: s.name)

    return render_template('7-states_list.html', states=states_sorted)


if __name__ == '__main__':
    app.run(debug=True)
