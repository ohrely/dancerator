from jinja2 import StrictUndefined

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db
from code_to_choreo import simple_trans
from app import app
import doctest

# Jinja, please tell me if you intend to fail
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Landing page"""

    return render_template("homepage.html")


@app.route('/new')
def generate():
    """Create dance, return page with results"""

    dance = simple_trans()
    print dance

    return render_template("new.html", dance=dance)


if __name__ == "__main__":

    connect_to_db(app)

    doctest.testmod(verbose=True)
