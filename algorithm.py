from model import Move, Type_, Chain, Progression
from model import connect_to_db, db
from server import app
from random import choice
import doctest

# base case: total dance is 64 counts
# later base case: penultimate move flows into final move

DANCE_LENGTH = 64


def pick_progression():
    """Randomly choose a first and last move from the database.

    >>> type(pick_progression())
    <type 'tuple'>
    """
    prog_list = db.session.query(Progression.last, Progression.first).all()
    last_move, first_move = choice(prog_list)

    return (last_move, first_move)


def len_left_init(last_move):
    """Initial determination of remaining beats to be filled by tree recursion.

    >>> len_left_init(u'hhey')
    56
    """
    minus_last = len_left(DANCE_LENGTH, last_move)

    return minus_last


def len_left(old_len_left, move):
    """Given the addition of a move to a partially-written dance, find remaining beats to be filled.

    >>> len_left(32, u'hhey')
    24
    """
    # TODO: unicode errors like woah.
    move_beats = db.session.query(Move.beats).filter(Move.move_code == u'move').one()
    beats_left = old_len_left - move_beats[0]

    return beats_left


def find_curr_values(key):
    """Given a move, return a randomly sorted list of possible next moves.

    Query database and randomly sort list of what comes back.

    >>> find_curr_values(u'llfb')
    [u'fchn', u'fal6', u'nswg', u'fdp6', u'lal6']
    """
    value_list = []

    # SQL queries are faster than SQLAlchemy queries - change if it's slow
    value_tups = db.session.query(Chain.value).filter(Chain.key == key).all()

    for value in value_tups:
        value_list.append(value[0])

    return value_list


# # TODO: for use when checking end-of-dance base cases
# def try_leaf(curr_key, beats_left, dance, last_move):


def build_dance(curr_key, beats_left, dance, last_move):
    """Build 'legal' dance using recursion to ensure constraint satisfaction
    """

    beats_left = len_left(beats_left, curr_key)
    curr_values = find_curr_values(curr_key)
    works = False
    last_move = last_move

    while not works:

        # Fail condition
        if beats_left < 0:
            print "too long"

        # Base case
        # TODO: move out to own function for testing ease
        if beats_left == 0:
            dance.append(curr_key)
            dance.append(last_move)
            works = True

        # Recursive call
        if beats_left > 0:
            dance.append(curr_key)
            for next_key in curr_values:
                build_dance(next_key, beats_left, dance, last_move)
        else:
            print("Something is wrong.")

    print "works = ", works
    return dance


def all_together_now():
    dance = []

    progression = pick_progression()
    last_move = progression[0]
    first_move = progression[1]
    # beats_left = len_left_init(last_move)
    # print beats_left

    # entire_dance = build_dance(first_move, beats_left, dance, last_move)

    # return entire_dance


if __name__ == "__main__":

    connect_to_db(app)
    print "Connected to DB."

    doctest.testmod(verbose=True)

    all_together_now()
