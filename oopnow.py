from model import Move, Type_, Chain, Progression
from model import connect_to_db, db
from server import app
from random import choice, shuffle
import doctest


class MoveObj(object):
    def __init__(self, move_code):
        self.move_code = move_code
        self.get_attributes()

    def get_attributes(self):
        type_query = db.session.query(Move.type_code).filter(Move.move_code == self.move_code).one()
        self.type_code = type_query[0]

        beats_query = db.session.query(Move.beats).filter(Move.move_code == self.move_code).one()
        self.beats = beats_query[0]

        name_query = db.session.query(Move.move_name).filter(Move.move_code == self.move_code).one()
        self.name = name_query[0]

        min_query = db.session.query(Type_.min_repeats).filter(Type_.type_code == self.type_code).one()
        self.min = min_query[0]

        max_query = db.session.query(Type_.max_repeats).filter(Type_.type_code == self.type_code).one()
        self.max = max_query[0]

        # self.move_lead = db.session.query(Move.move_lead).filter(Move.move_code == self.move_code).one()
        # self.move_follow = db.session.query(Move.move_follow).filter(Move.move_code == self.move_code).one()
        # self.same_side = db.session.query(Move.same_side).filter(Move.move_code == self.move_code).one()

        self.values = self.get_values()

    def get_values(self):
        values = db.session.query(Chain.value).filter(Chain.key_ == self.move_code).all()
        values_list = []
        for value in values:
            values_list.append(value)
        return values_list

    def __repr__(self):

        return "<MoveObj move_code={}>".format(self.move_code)


# class Dance(object):
#     def __init__(self):


def pull_move_codes():
    all_codes = db.session.query(Move.move_code).all()
    return all_codes


def make_moves(all_moves):
    move_dict = {}
    for code in all_moves:
        move_code = code[0]
        move_dict[move_code] = MoveObj(move_code)
    return move_dict


def do_it_all():
    all_moves = pull_move_codes()

    da_dict = make_moves(all_moves)
    print da_dict


if __name__ == "__main__":

    connect_to_db(app)
    print "Connected to DB."

    doctest.testmod(verbose=True)

    do_it_all()
