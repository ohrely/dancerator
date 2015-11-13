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


class DanceObj(object):
    def __init__(self, move_dict):
        self.move_dict = move_dict
        self.dance_moves = self.all_together_now()

    def pick_progression(self):
        """Randomly choose a first and last move from the database.

        >>> type(self.pick_progression())
        <type 'tuple'>
        """
        prog_list = db.session.query(Progression.last, Progression.first, Progression.start).all()
        last_move, first_move, start_position = choice(prog_list)

        return (last_move, first_move, start_position)

    def len_left_init(self, last_move):

        move_beats = self.move_dict[last_move].beats
        minus_last = DANCE_LENGTH - move_beats

        return minus_last

    def count_dance(self, dance):
        """Count dance from build_dance; should be 64 beats.

        >>> count_dance([u'ngrm', u'nswg', u'llfb', u'nswg', u'lal6', u'pswg', u'pswg', u'nrlt', u'fchn', u'crl3'])
        64
        """
        count = 0
        for each_move in dance:
            move_time = self.move_dict[each_move].beats
            count += move_time

        return count

    def try_last_flow(self, curr_key, last_move):
        """Check that potential penultimate move flows into final move.

        >>> try_last_flow("pbal", "pcal")
        True

        >>> try_last_flow("pbal", "nswg")
        DIDN'T FLOW
        False
        """
        curr_values = self.move_dict[curr_key].values
        # if last_move in curr_values && curr_position = last_position:
        if last_move in curr_values:
            works = True
        else:
            print "DIDN'T FLOW"
            works = False
        return works

    def try_leaf(self, curr_key, last_move, dance):
        potential_whole = list(dance)
        potential_whole.append(curr_key)

        if self.try_last_flow(curr_key, last_move) is True:
            return True
        else:
            return False

    def build_dance(self):
        """
        """
        return dance, works

    def all_together_now(self):
        """Run helper methods and build_dance.

        """
        dance = []

        last_move, first_move, start_position = self.pick_progression()
        beats_left = self.len_left_init(last_move)
        print "BEATS TO FILL: ", beats_left

        entire_dance, works = self.build_dance(first_move, dance, last_move)
        print "DANCE CREATED: ", entire_dance

        total_time = self.count_dance(entire_dance, self.move_dict)
        print "TOTAL TIME: ", total_time
        # If something goes wrong, scrap it and try again.
        if total_time != 64:
            print ". . . . . . . . . . . . . . . . . . ."
            print ". . . . . . . . . . . . . . . . . . ."
            print ". . . . . . . . . . . . . . . . . . ."
            print ". . . . . . . . . . . . . . . . . . ."
            print ". . . . . . . . . . . . . . . . . . ."
            self.all_together_now()
        else:
            pass

        return entire_dance

    def create_display_string(self, dance_moves):
        """Convert dance codes into choreography.

        """
        return dance_moves


def pull_move_codes():
    """Queries database for all move codes.
    """
    all_codes = db.session.query(Move.move_code).all()
    return all_codes


def make_moves(all_moves):
    """Creates dictionary of all MoveObj objects.
    """
    move_dict = {}
    for code in all_moves:
        move_code = code[0]
        move_dict[move_code] = MoveObj(move_code)
    return move_dict


def do_it_all():
    all_moves = pull_move_codes()

    da_dict = make_moves(all_moves)
    print da_dict

    new_dance = DanceObj(da_dict)
    print new_dance


if __name__ == "__main__":

    connect_to_db(app)
    print "Connected to DB."

    doctest.testmod(verbose=True)

    do_it_all()
