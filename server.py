from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db
from model import Creation
from code_to_choreo import make_choreo, simple_trans, make_title
import doctest

app = Flask(__name__)

app.secret_key = "contra"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Landing page"""

    return render_template("homepage.html")


@app.route('/new')
def generate():
    """Create dance, write to db, return page with results"""

    title = make_title()
    pre_trans, dance, the_prog = make_choreo()
    pre_trans = ",".join(pre_trans)

    db_dance = Creation(dance_name=title, choreo=pre_trans, progression=the_prog)

    db.session.add(db_dance)
    db.session.commit()

    dance_id = db.session.query(Creation.dance_id).filter(Creation.choreo == pre_trans).first()[0]
    print "DANCE_ID IS: ", dance_id
    dance_url = "dance/{}".format(dance_id)
    print "REDIRECTING TO ", dance_url

    return redirect(dance_url)


@app.route('/dance/<int:dance_id>')
def display(dance_id):
    """Given the id of a dance in the creations table, display choreo page"""

    creation = db.session.query(Creation).get(dance_id)
    title = creation.dance_name
    pre_trans = creation.choreo
    pre_trans = pre_trans.split(",")
    dance = simple_trans(dance=pre_trans)

    return render_template("dance.html", dance=dance, title=title)


@app.route('/ack')
def thanks():
    """Acknowlegements page"""

    return render_template("ack.html")

if __name__ == "__main__":

    app.debug = True
    connect_to_db(app)
    # DebugToolbarExtension(app)
    app.run()

    # doctest.testmod(verbose=True)
