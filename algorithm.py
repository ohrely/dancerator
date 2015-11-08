from model import Move, Type_, Chain, Progression
from model import connect_to_db, db
from server import app
from random import choice
import doctest

# base case: total dance is 64 counts
# later base case: penultimate move flows into final move

DANCE_LENGTH = 64

# class Move(object):
#     def __init__(self, key=None, values=None, length=None):
#         self.key = key
#         self.values = values
#         self.length = length


def pick_progression():
    """Randomly choose a first and last move from the database.

    >>> pick_progression()
    ["yassss"]

    """
    prog_list = db.session.query(Progression.last, Progression.first).all()
    last_move, first_move = choice(prog_list)

    return (last_move, first_move)


dance = []

# TODO Nest inside a function that gets called under 'if __name__ = "__main__":'
# progression = pick_progression()
# last_move = progression[0]
# first_move = progression[1]


def len_left_init(last_move):
    """Initial determination of remaining beats to be filled by tree recursion.

    >>> len_left_init(u'hhey')
    56
    """
    minus_last = len_left(DANCE_LENGTH, last_move)

    return minus_last


def len_left(len_left, move):
    """Given the addition of a move to a partially-written dance, find remaining beats to be filled.

    >>> len_left(32, u'hhey')
    24
    """
    move_beats = db.session.query(Move.beats).filter(Move.move_code == move).one()
    len_left -= move_beats[0]

    return len_left


# def find_curr_values(key):
#     """Given a move, return a randomly sorted list of possible next moves.

#     Query database and randomly sort list of what comes back.

#     >>> find_curr_values(u'llfb')
#     [u'fchn', u'fal6', u'nswg', u'fdp6', u'lal6']
#     """
#     value_list = []

#     # SQL queries are faster than SQLAlchemy queries - change if it's slow
#     value_tups = db.session.query(Chain.value).filter(Chain.key == key).all()

#     for value in value_tups:
#         value_list.append(value[0])

#     return value_list


# # For testing - not real data
# llfb = Move(llfb, pswg, 4)
# pswg = Move(pswg, fchn, 8)

# def build_dance(curr_key, len_left, dance):
#     """Build 'legal' dance using recursion to ensure constraint satisfaction

#     >>>build_dance(llfb, 8, [what, yass])
#     [what, yass, llfb, pswg]

#     """

#     # find out time left if current move were added to dance
#     len_left = len_left - curr_key.length
#     curr_values = find_curr_values(curr_key)

#     # fail condition
#     if len_left < 0:
#         print "too long"
#         return

#     # base case - move out to own function for testing ease
#     if len_left == 0:
#         dance.append(curr_key)
#         dance.append(last_move)
#         return dance
#         # TODO - ensure that this stops the function

#     # recursive call
#     if len_left > 0:
#         dance.append(curr_key)
#         for next_key in curr_values:
#             build_dance(next_key, len_left, dance)

#     return dance


# print build_dance(first_move, len_left, dance)

if __name__ == "__main__":

    connect_to_db(app)
    print "Connected to DB."

    doctest.testmod(verbose=True)
