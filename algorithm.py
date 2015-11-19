from model import Move, Type_, Chain, Progression
from model import connect_to_db, db
from random import choice, shuffle
import doctest


DANCE_LENGTH = 64


class MoveObj(object):
    def __init__(self, move_code):
        self.move_code = move_code
        self.get_attributes()

    def get_attributes(self):
        self.type_code, self.beats, self.name = db.session.query(Move.type_code, Move.beats, Move.move_name).filter(Move.move_code == self.move_code).one()
        self.move_lead, self.move_follow, self.same_side = db.session.query(Move.leads_move, Move.follows_move, Move.same_side).filter(Move.move_code == self.move_code).one()

        self.min, self.max = db.session.query(Type_.min_repeats, Type_.max_repeats).filter(Type_.type_code == self.type_code).one()

        self.orphanable = self.orphanable()
        self.values = self.get_values()

    def get_values(self):
        """Query chains table for moves that may follow this one.
        """
        values = db.session.query(Chain.value).filter(Chain.key_ == self.move_code).all()
        values_list = []
        for value in values:
            values_list.append(value[0])
        return values_list

    def orphanable(self):
        """Determine whether move needs special treatment to avoid orphaning.
        """
        return self.min != 0

    def __repr__(self):
        return "<MoveObj move_code={}>".format(self.move_code)

# def defaultLogger(stuff):
#     print stuff

# def noopLogger(stuff):


class DanceObj(object):
    # def __init__(self, move_dict, logger=defaultLogger):
    def __init__(self, move_dict):
        self.move_dict = move_dict
        self.last_move, self.first_move, self.start = self.pick_progression()
        self.beats_to_fill = self.len_left_init(self.last_move)
        self.dance_moves = self.all_together_now()

    def pick_progression(self):
        """Randomly choose a first and last move from the database.
        """
        prog_list = db.session.query(Progression.last, Progression.first, Progression.start).all()
        last_move, first_move, start_position = choice(prog_list)

        return (last_move, first_move, start_position)

    def len_left_init(self, last_move):
        """Initial determination of remaining beats to be filled by tree recursion.
        """
        move_beats = self.move_dict[last_move].beats
        minus_last = DANCE_LENGTH - move_beats

        return minus_last

    def count_dance(self, dance):
        """Count dance from build_dance; should be 64 beats.
        """
        count = 0
        for each_move in dance:
            move_time = self.move_dict[each_move].beats
            count += move_time

        return count

    def find_follows(self, dance):
        """Given a partially-built dance, find the follows.
        """
        count = 0
        for each_move in dance:
            follows_move = self.move_dict[each_move].move_follow
            count += follows_move
            count = count % 4

        return count

    def find_leads(self, dance):
        """Given a partially-built dance, find the follows.
        """
        count = 0
        for each_move in dance:
            leads_move = self.move_dict[each_move].move_lead
            count += leads_move
            count = count % 4

        return count

    def try_positions(self, test_value, dance):
        """Check that dancers are in appropriate position to flow into test_value.
        """
        follows_at = self.find_follows(dance)
        follows_move = self.move_dict[test_value].move_follow
        follows_to = (follows_at + follows_move) % 4
        print "FOLLOWS MOVE ", follows_move, "FROM ", follows_at, "TO ", follows_to

        leads_at = self.find_leads(dance)
        leads_move = self.move_dict[test_value].move_lead
        leads_to = (leads_at + leads_move) % 4
        print "LEADS MOVE ", leads_move, "FROM ", leads_at, "TO ", leads_to

        start_same = self.move_dict[test_value].same_side
        print "START SAME: ", start_same

        # do set math to check that follow/lead positions are or are not on same side
        if start_same == 2:
            return True
        # elif start_same < 10:
        #     positions = set(leads_at, follows_at)
        #     if start_same == 1:
        #         if positions
            # set math
        # else:
        #     if start_same is True:
        #         if 1 == 1:
        #         # if (set math):
        #             return True
        #         else:
        #             return False
        #     elif start_same is False:
        #         if 1 == 1:
        #         # if (set math):
        #             return True
        #         else:
        #             return False
        return True

    def too_many(self, test_value, new_dance):
        """Check that the addition of a move does not violate the max_repeats rules for type.
        """
        test_type = self.move_dict[test_value].type_code
        max_repeats = self.move_dict[test_value].max
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

    def orphan_wrangling(self, curr_key, dance, curr_len):
        """
        """
        if self.move_dict[curr_key].orphanable is False:
            curr_values = self.move_dict[curr_key].values
            shuffle(curr_values)
        elif self.move_dict[curr_key].orphanable is True:
            if self.move_dict[curr_key].type_code != self.move_dict[dance[-1]].type_code:
                if curr_len in [16, 32, 48]:
                    print curr_key, " NEEDS MORE TIME"
                    return None
                else:
                    curr_values = [curr_key]
                    print "TO PREVENT ORPHANS, ", curr_values, "IS THE ONLY CURRENT VALUE"
            elif self.move_dict[curr_key].type_code == self.move_dict[dance[-1]].type_code:
                if self.move_dict[curr_key].type_code == 'swing' and curr_len not in [16, 32, 48]:
                    curr_values = [curr_key]
                    print "TO FILL THE BUCKET, ", curr_values, " IS THE ONLY CURRENT VALUE"
                else:
                    curr_values = self.move_dict[curr_key].values
                    shuffle(curr_values)
            else:
                print "THE ORPHANS ARE MAKING TROUBLE"
                return None

        return curr_values

    def try_last_flow(self, curr_key, curr_values, last_move):
        """Check that final move is in values for potential penultimate move.
        """
        if last_move in curr_values:
            works = True
        else:
            print "DIDN'T FLOW - VALUES"
            works = False

        return works

    def try_last_position(self, start, dance):
        """Check that potential penultimate move leaves dancers in correct position for final move.
        """
        if self.find_follows(dance) == start:
            works = True
        else:
            print "DIDN'T FLOW - POSITIONS"
            works = False

        return works

    def try_leaf(self, curr_key, curr_values, last_move, start, dance):
        """Check all end-of-dance base cases.
        """
        potential_whole = list(dance)
        potential_whole.append(curr_key)

        if self.try_last_flow(curr_key, curr_values, last_move) is True and self.try_last_position(start, dance) is True:
            return True
        else:
            return False

    # def build_dance(self, curr_key, dance, follow_pos, last_move):
    def build_dance(self, curr_key, last_move, start, dance=None):
        """
        """
        if not dance:
            dance = []

        new_dance = list(dance)
        new_dance.append(curr_key)
        curr_len = self.count_dance(new_dance)
        beats_left = self.beats_to_fill - curr_len

        works = False

        # Prevent orphans, ensure that swings fill buckets
        curr_values = self.orphan_wrangling(curr_key, dance, curr_len)

        if not curr_values:
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
            if self.try_leaf(curr_key, curr_values, last_move, start, dance) is True:
                dance.append(curr_key)
                dance.append(last_move)
                works = True
            else:
                works = False
            return dance, works
        # Recursive call
        elif beats_left > 0:
            for next_key in curr_values:
                print "............................................................."
                print "BEATS TO FILL: ", beats_left
                print "DANCE: ", new_dance
                print "TRYING: ", next_key, "(", self.move_dict[next_key].beats, ") beats"
                if self.too_many(next_key, new_dance) is False:
                    if self.try_positions(next_key, new_dance) is True:
                        dance, works = self.build_dance(next_key, last_move, start, new_dance)
                        if works is True:
                            break
                    else:
                        print "POSITIONS DON'T WORK"
                        return dance, works
                else:
                    print "TOO MANY", self.move_dict[next_key].type_code, "NOT ADDING MORE"
                    return dance, works
        else:
            print "----------Something is wrong.----------"
            pass

        return dance, works

    def all_together_now(self):
        """Run build_dance and check outcomes.
        """
        print "PROGRESSION: ", self.last_move, self.first_move, self.start
        print "BEATS TO FILL: ", self.beats_to_fill

        # entire_dance, works = self.build_dance(self.first_move, empty_dance, follow_start, self.last_move)
        entire_dance, works = self.build_dance(curr_key=self.first_move, last_move=self.last_move, start=self.start)
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

    from server import app
    connect_to_db(app)
    print "Connected to DB."

    # doctest.testmod(verbose=True)

    do_it_all()
