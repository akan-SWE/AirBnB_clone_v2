#!/usr/bin/python3
"""
Module: 7-states_list

Flask web application

Routes:
    '/states_list' - Displays a HTML page containing all States objects

Function:
    clean_session: Remove the current session after each request
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def clean_session(var):
    """
    Remove the current session after each request
    """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Display a HTML page that lists all States objects
    """
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(debug=True)
