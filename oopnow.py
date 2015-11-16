from model import Move, Type_, Chain, Progression
from model import connect_to_db, db
from app import app
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

        self.orphanable = self.orphanable()

        # self.move_lead = db.session.query(Move.move_lead).filter(Move.move_code == self.move_code).one()
        # self.move_follow = db.session.query(Move.move_follow).filter(Move.move_code == self.move_code).one()
        # self.same_side = db.session.query(Move.same_side).filter(Move.move_code == self.move_code).one()

        self.values = self.get_values()

    def get_values(self):
        values = db.session.query(Chain.value).filter(Chain.key_ == self.move_code).all()
        values_list = []
        for value in values:
            values_list.append(value[0])
        return values_list

    def orphanable(self):
        if self.min == 0:
            return False
        else:
            return True

    def __repr__(self):
        return "<MoveObj move_code={}>".format(self.move_code)


class DanceObj(object):
    def __init__(self, move_dict):
        self.move_dict = move_dict
        # print "MOVE DICT: ", self.move_dict
        self.last_move = self.pick_progression()[0]
        self.first_move = self.pick_progression()[1]
        self.start_position = self.pick_progression()[2]
        print "PROGRESSION:", self.pick_progression()
        self.beats_to_fill = self.len_left_init(self.last_move)
        self.dance_moves = self.all_together_now()

    def pick_progression(self):
        """Randomly choose a first and last move from the database.

        # >>> type(pick_progression())
        # <type 'tuple'>
        """
        prog_list = db.session.query(Progression.last, Progression.first, Progression.start).all()
        last_move, first_move, start_position = choice(prog_list)

        return (last_move, first_move, start_position)

    def len_left_init(self, last_move):
        """Initial determination of remaining beats to be filled by tree recursion.

        >>> self.len_left_init(u'hhey')
        56
        """
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

    def too_many(self, test_key, new_dance):
        """Check that the addition of a move does not violate the max_repeats rules for type.
        """

        test_type = self.move_dict[test_key].type_code
        max_repeats = self.move_dict[test_key].max
        print "TYPE: ", test_type, "MAX REPEATS:", max_repeats

        if self.move_dict[new_dance[-1]].type_code != test_type:
            return False
        elif max_repeats == 0:
            return True
        else:
            danger_zone = new_dance[-(max_repeats + 1):]
            print "DANGER ZONE: ", danger_zone

            repeats = 0
            for old_move in danger_zone:
                if self.move_dict[old_move].type_code == test_type:
                    repeats += 1
            print "REPEATS: ", repeats

            if repeats == (max_repeats + 1):
                return True
            else:
                return False

    def try_last_flow(self, curr_key, curr_values, last_move):
        """Check that potential penultimate move flows into final move.

        >>> try_last_flow("pbal", "pcal")
        True

        >>> try_last_flow("pbal", "nswg")
        DIDN'T FLOW
        False
        """
        # if last_move in curr_values && curr_position = last_position:
        if last_move in curr_values:
            works = True
        else:
            print "DIDN'T FLOW"
            works = False
        return works

    def try_leaf(self, curr_key, curr_values, last_move, dance):
        """Check all end-of-dance base cases.
        """
        potential_whole = list(dance)
        potential_whole.append(curr_key)

        if self.try_last_flow(curr_key, curr_values, last_move) is True:
            return True
        else:
            return False

    # def build_dance(self, curr_key, dance, follow_pos, last_move):
    def build_dance(self, curr_key, dance, last_move):
        """
        """
        new_dance = list(dance)
        new_dance.append(curr_key)
        curr_len = self.count_dance(new_dance)
        beats_left = self.beats_to_fill - curr_len

        # follows_to = (follow_pos + self.move_dict[curr_key].move_follow) % 4
        # print "FOLLOW 1 IS AT: ", follows_to

        works = False

        # Prevent orphans
        if self.move_dict[curr_key].orphanable is False:
            curr_values = self.move_dict[curr_key].values
            shuffle(curr_values)
        elif self.move_dict[curr_key].orphanable is True:
            if self.move_dict[curr_key].type_code != self.move_dict[dance[-1]].type_code:
                curr_values = [curr_key]
                print "TO PREVENT ORPHANS, ", curr_values, "IS THE ONLY CURRENT VALUE"
            elif self.move_dict[curr_key].type_code == self.move_dict[dance[-1]].type_code:
                curr_values = self.move_dict[curr_key].values
                shuffle(curr_values)
            else:
                print "THE ORPHANS ARE MAKING TROUBLE"
                return dance, works

        # Fail condition
        if beats_left < 0:
            print "TOO LONG"
            return dance, works
        elif self.count_dance(dance) < 16 < curr_len:
            print "CROSSES 16"
            return dance, works
        elif self.count_dance(dance) < 32 < curr_len:
            print "CROSSES 32"
            return dance, works
        elif self.count_dance(dance) < 48 < curr_len:
            print "CROSSES 48"
            return dance, works
        # Base case
        elif beats_left == 0:
            if self.try_leaf(curr_key, curr_values, last_move, dance) is True:
                dance.append(curr_key)
                dance.append(last_move)
                works = True
            else:
                works = False
            return dance, works
        # Recursive call
        elif beats_left > 0:
            for next_key in curr_values:
                if self.too_many(next_key, new_dance) is False:
                    print "............................................................."
                    print "DANCE: ", new_dance
                    print "BEATS TO FILL: ", beats_left
                    print "TRYING: ", next_key, "(", self.move_dict[next_key].beats, ") beats"
                    # print "BEATS FILLED: ", curr_len
                    dance, works = self.build_dance(next_key, new_dance, last_move)
                    if works is True:
                        break
                else:
                    print "............................................................."
                    print "TOO MANY", self.move_dict[next_key].type_code, "NOT ADDING MORE"
                    return dance, False
        else:
            print "----------Something is wrong.----------"
            pass

        return dance, works

    def all_together_now(self):
        """Run helper methods and build_dance.

        """
        empty_dance = []
        # follow_start = 0

        print "BEATS TO FILL: ", self.beats_to_fill

        # entire_dance, works = self.build_dance(self.first_move, empty_dance, follow_start, self.last_move)
        entire_dance, works = self.build_dance(self.first_move, empty_dance, self.last_move)
        print "DANCE CREATED: ", entire_dance

        total_time = self.count_dance(entire_dance)
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


def make_moves():
    """Creates dictionary of all MoveObj objects.
    """
    all_moves = pull_move_codes()

    move_dict = {}
    for code in all_moves:
        move_code = code[0]
        move_dict[move_code] = MoveObj(move_code)
    return move_dict


def do_it_all():
    da_dict = make_moves()
    new_dance = DanceObj(da_dict)
    return new_dance.dance_moves, da_dict


if __name__ == "__main__":

    connect_to_db(app)
    print "Connected to DB."

    doctest.testmod(verbose=True)

    do_it_all()
