from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db

app = Flask(__name__)

app.secret_key = "contra"

if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()
