from model import connect_to_db, db
from server import app
import oopnow
import doctest


def make_dance():
    dance_moves, da_dict = oopnow.do_it_all()
    return dance_moves, da_dict


def simple_trans():
    dance, da_dict = make_dance()
    translation = []

    for move in dance:
        move_name = da_dict[move].name
        translation.append(move_name)

    print translation
    return translation


if __name__ == "__main__":

    connect_to_db(app)
    print "Connected to DB."

    doctest.testmod(verbose=True)

    simple_trans()
