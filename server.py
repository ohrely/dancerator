from jinja2 import StrictUndefined

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Move, Progression
# import algorithm

app = Flask(__name__)

app.secret_key = "contra"

# Jinja, please tell me if you intend to fail
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Landing page"""

    return render_template("homepage.html")


@app.route('/new')
def generate():
    """Create dance, return page with results"""

    dance = algorithm.all_together_now()
    print dance

    return render_template("new.html", dance=dance)


if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()
