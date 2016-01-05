from model import Progression
from model import connect_to_db, db
from random import choice, shuffle


def make_medley(prog=None, total=None):
    """Select dances from the database that would work as a medley.
    """
    if not prog:
        random_prog = choice(db.session.query(Progression.last, Progression.first).all())

        prog = random_prog[0] + ", " + random_prog[1]

    print prog

    if not total:
        total = 3

    return

if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."

    # doctest.testmod(verbose=True)

    make_medley()
