from model import Move, Type_, Chain, Progression
from model import connect_to_db, db
from server import app
from random import choice, shuffle
import doctest


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
    move_beats = db.session.query(Move.beats).filter(Move.move_code == last_move).one()
    minus_last = DANCE_LENGTH - move_beats[0]

    return minus_last


def move_len(latest_move):
    """Query db for move length.

    May be replaced by dictionary if queries are too slow.
    """
    move_beats = db.session.query(Move.beats).filter(Move.move_code == latest_move).one()
    move_beats = move_beats[0]

    return move_beats


def find_curr_values(key_):
    """Given a move, return a shuffled list of possible next moves (from chains query).

    >>> len(find_curr_values(u'llfb'))
    5
    """
    value_list = []

    # SQL queries are faster than SQLAlchemy queries - change if it's slow
    value_tups = db.session.query(Chain.value).filter(Chain.key_ == key_).all()

    for value in value_tups:
        value_list.append(value[0])

    shuffle(value_list)

    return value_list


def type_move(move):
    """Query database for a move's type_code.

    >>> type_move(u'nbal')
    u'bal'
    """
    type_ = db.session.query(Move.type_code).filter(Move.move_code == move).one()
    type_ = type_[0]
    return type_


def too_many(move, dance):
    """Check that the addition of a move does not violate the max_repeats rules for type.

    >>> too_many(u'nswg', [u'nbal', u'nswg', u'nswg', u'llfb'])
    TYPE:  swing MAX REPEATS: 3
    False

    >>> too_many(u'llfb', [u'nbal', u'nswg', u'nswg', u'llfb'])
    TYPE:  lines MAX REPEATS: 0
    True

    >>> too_many(u'nswg', [u'nbal', u'nswg', u'nswg', u'nswg', u'nswg'])
    TYPE:  swing MAX REPEATS: 3
    DANGER ZONE:  [u'nswg', u'nswg', u'nswg', u'nswg']
    REPEATS:  4
    True

    >>> too_many(u'nswg', [u'nswg', u'nswg', u'nswg'])
    TYPE:  swing MAX REPEATS: 3
    DANGER ZONE:  [u'nswg', u'nswg', u'nswg']
    REPEATS:  3
    False
    """
    type_ = type_move(move)
    max_repeats = db.session.query(Type_.max_repeats).filter(Type_.type_code == type_).first()[0]
    print "TYPE: ", type_, "MAX REPEATS:", max_repeats

    if type_move(dance[-1]) != type_:
        return False
    elif max_repeats == 0:
        return True
    else:
        danger_zone = dance[-(max_repeats + 1):]
        print "DANGER ZONE: ", danger_zone

        repeats = 0
        for old_move in danger_zone:
            if type_move(old_move) == type_:
                repeats += 1
        print "REPEATS: ", repeats

        if repeats == (max_repeats + 1):
            return True
        else:
            return False


def try_last_flow(curr_key, last_move):
    """Check that potential penultimate move flows into final move.

    >>> try_last_flow("pbal", "pcal")
    True

    >>> try_last_flow("pbal", "nswg")
    DIDN'T FLOW
    False
    """
    curr_values = find_curr_values(curr_key)
    # if last_move in curr_values && curr_position = last_position:
    if last_move in curr_values:
            works = True
    else:
        print "DIDN'T FLOW"
        works = False
    return works


def try_leaf(curr_key, last_move, dance):
    """Check end-of-dance base cases.

    >>> try_leaf(u'pbal', u'lal6', [u'nswg', u'nswg', u'hhey'])
    DIDN'T FLOW
    False

    >>> try_leaf(u'nswg', u'nswg', [u'nbal', u'nswg', u'nswg', u'nswg'])
    TYPE:  swing MAX REPEATS: 3
    DANGER ZONE:  [u'nswg', u'nswg', u'nswg', u'nswg']
    REPEATS:  4
    False

    >>> try_leaf(u'nswg', u'nswg', [u'nbal', u'nswg', u'nswg'])
    TYPE:  swing MAX REPEATS: 3
    DANGER ZONE:  [u'nbal', u'nswg', u'nswg', u'nswg']
    REPEATS:  3
    True
    """
    potential_whole = [move for move in dance]
    potential_whole.append(curr_key)

    if try_last_flow(curr_key, last_move) is True:
        if too_many(last_move, potential_whole) is False:
            return True
        else:
            return False
    else:
        return False


def count_dance(dance):
    """Count dance from build_dance; should be 64 beats.

    >>> count_dance([u'ngrm', u'nswg', u'llfb', u'nswg', u'lal6', u'pswg', u'pswg', u'nrlt', u'fchn', u'crl3'])
    64
    """
    count = 0
    for each_move in dance:
        move_time = move_len(each_move)
        count += move_time

    return count


def build_dance(curr_key, dance, last_move):
    """Build 'legal' dance using recursion to ensure constraint satisfaction
    """

    len_before = count_dance(dance)
    curr_len = len_before + move_len(curr_key)
    beats_left = len_left_init(last_move) - curr_len
    works = False

    # Fail condition
    if beats_left < 0:
        print "TOO LONG"
        return dance, False
    elif count_dance(dance) < 16 < curr_len:
        print "CROSSES 16"
        return dance, False
    elif count_dance(dance) < 32 < curr_len:
        print "CROSSES 32"
        return dance, False
    elif count_dance(dance) < 48 < curr_len:
        print "CROSSES 48"
        return dance, False
    # Base case
    elif beats_left == 0:
        if try_leaf(curr_key, last_move, dance) is True:
            dance.append(curr_key)
            dance.append(last_move)
            works = True
            return dance, works
    # Recursive call
    elif beats_left > 0:
        # if curr_key.orphanable is False or curr_key.orphaned == "safe":
        curr_values = find_curr_values(curr_key)
        # elif curr_key.orphaned == "bad":
        #     return dance[:-1], False
        # elif curr_key.orphaned == "danger":
            # curr_values = [curr_key]

        new_dance = list(dance)
        new_dance.append(curr_key)

        for next_key in curr_values:
            if too_many(next_key, new_dance) is False:
                print "............................................................."
                print "DANCE: ", new_dance
                print "BEATS TO FILL: ", beats_left
                print "TRYING: ", next_key, "(", move_len(next_key), ") beats"
                print "BEATS FILLED: ", count_dance(new_dance)
                dance, works = build_dance(next_key, new_dance, last_move)
                if works is True:
                    break
            else:
                print "............................................................."
                print "TOO MANY", type_move(next_key), "NOT ADDING MORE"
                return dance, False
    else:
        print "---------Something is wrong.---------"
        pass

    return dance, works


def all_together_now():
    """Run helper functions and build_dance.

    May become a class later.
    """
    dance = []

    last_move, first_move = pick_progression()
    # last_position = db.session.query(Progression.start).filter(Progression.last == last_move).first()
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


if __name__ == "__main__":

    connect_to_db(app)
    print "Connected to DB."

    doctest.testmod(verbose=True)

    all_together_now()
