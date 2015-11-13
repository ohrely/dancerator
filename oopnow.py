from model import Move, Type_, Chain, Progression
from model import connect_to_db, db
from server import app
from random import choice, shuffle
import doctest


DANCE_LENGTH = 64


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


class Dance(object):
    def __init__(self):
        self.dance_moves = all_together_now()

    def pick_progression():
        """Randomly choose a first and last move from the database.

        >>> type(pick_progression())
        <type 'tuple'>
        """
        prog_list = db.session.query(Progression.last, Progression.first, Progression.start).all()
        last_move, first_move, start_position = choice(prog_list)

        return (last_move, first_move, start_position)

    def len_left_init(last_move):

        move_beats = move_dict[last_move].beats
        minus_last = DANCE_LENGTH - move_beats

        return minus_last

    def count_dance(dance):
        """Count dance from build_dance; should be 64 beats.

        >>> count_dance([u'ngrm', u'nswg', u'llfb', u'nswg', u'lal6', u'pswg', u'pswg', u'nrlt', u'fchn', u'crl3'])
        64
        """
        count = 0
        for each_move in dance:
            move_time = move_dict[move].beats
            count += move_time

        return count

    def build_dance():
        return dance, works

    def all_together_now():
        """Run helper methods and build_dance.

        """
        dance = []

        last_move, first_move, start_position = pick_progression()
        beats_left = len_left_init(last_move)
        print "BEATS TO FILL: ", beats_left

        entire_dance, works = build_dance(first_move, dance, last_move)
        print "DANCE CREATED: ", entire_dance

        total_time = count_dance(entire_dance)
        print "TOTAL TIME: ", total_time
        # If something goes wrong, scrap it and try again.
        if total_time != 64:
            print ". . . . . . . . . . . . . . . . . . ."
            print ". . . . . . . . . . . . . . . . . . ."
            print ". . . . . . . . . . . . . . . . . . ."
            print ". . . . . . . . . . . . . . . . . . ."
            print ". . . . . . . . . . . . . . . . . . ."
            all_together_now()
        else:
            pass

        return entire_dance

    def create_display_string(dance_moves):



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
