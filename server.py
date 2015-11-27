from jinja2 import StrictUndefined

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db
from code_to_choreo import simple_trans, make_title
import doctest

app = Flask(__name__)

app.secret_key = "contra"

# Jinja, please tell me if you intend to fail
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Landing page"""

    return render_template("next_homepage.html")


@app.route('/new')
def generate():
    """Create dance, return page with results"""

    title = make_title()
    print title
    dance = simple_trans()
    print dance

    return render_template("next_new.html", dance=dance, title=title)


if __name__ == "__main__":

    app.debug = True
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run()

    doctest.testmod(verbose=True)
