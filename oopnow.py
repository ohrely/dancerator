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
    #     self.move_type = db.session.query(Move.type_code).filter(Move.move_code == move).one()
    #     self.beats = db.session.query(Move.beats).filter(Move.move_code == latest_move).one()

    #     self.name = TODO
    #     self.values = self.get_values()

    # def get_values(self):
    #     values = db.session.query(Chain.value).filter(Chain.key == self.move_code).all()
    #     values_list = []
    #     for value in values:
    #         values_list.append(value)
    #     return values_list

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
