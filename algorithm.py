from model import Move, Type_, Chain, Progression
from model import connect_to_db, db
from server import app
from random import choice, shuffle
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
    move_beats = db.session.query(Move.beats).filter(Move.move_code == last_move).one()
    minus_last = DANCE_LENGTH - move_beats[0]

    return minus_last


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
    # print key_, value_list

    return value_list


def try_last_flow(curr_key, last_move):
    """Check that potential penultimate move flows into final move.

    >>> try_last_flow("pbal", "pcal")
    True

    >>> try_last_flow("pbal", "nswg")
    DIDN'T FLOW
    False
    """
    curr_values = find_curr_values(curr_key)
    if last_move in curr_values:
        works = True
    else:
        print "DIDN'T FLOW"
        works = False
    return works


# TODO: for use when checking end-of-dance base cases
def try_leaf(curr_key, last_move):
    """Check end-of-dance base cases.

    >>> try_leaf("pbal", "pcal")
    True

    >>> try_leaf("pbal", "nswg")
    DIDN'T FLOW
    False
    """
    if try_last_flow(curr_key, last_move) is True:
        return True
    else:
        return False


def build_dance(curr_key, beats_left, dance, last_move):
    """Build 'legal' dance using recursion to ensure constraint satisfaction
    """

    move_beats = db.session.query(Move.beats).filter(Move.move_code == curr_key).one()
    beats_left = len_left_init(last_move) - (count_dance(dance) + move_beats[0])
    curr_values = find_curr_values(curr_key)
    works = False
    last_move = last_move

    # Fail condition
    if beats_left < 0:
        print "TOO LONG: ", dance
        return dance[:-1], False
    # Base case
    elif beats_left == 0:
        if try_leaf(curr_key, last_move) is True:
            dance.append(curr_key)
            dance.append(last_move)
            works = True
            return dance, works
    # Recursive call
    elif beats_left > 0:
        dance.append(curr_key)
        for next_key in curr_values:
            print "DANCE: ", dance, "TRYING:", next_key, "BEATS:", beats_left
            print "............................................................."
            dance, works = build_dance(next_key, beats_left, dance, last_move)
            if works is True:
                break
    else:
        print "---------Something is wrong.---------"
        pass

    return dance, works


def count_dance(dance):
    """Count dance from build_dance; should be 64 beats.

    >>> count_dance([u'ngrm', u'nswg', u'llfb', u'nswg', u'lal6', u'pswg', u'pswg', u'nrlt', u'fchn', u'crl3'])
    64
    """
    count = 0
    for mv in dance:
        mv_time = db.session.query(Move.beats).filter(Move.move_code == mv).one()
        count += mv_time[0]

    return count


def all_together_now():
    """Run helper functions and build_dance.

    May become a class later.
    """
    dance = []

    progression = pick_progression()
    last_move = progression[0]
    first_move = progression[1]
    beats_left = len_left_init(last_move)
    print beats_left

    entire_dance, works = build_dance(first_move, beats_left, dance, last_move)
    print "DANCE CREATED: ", entire_dance
    total_time = count_dance(entire_dance)
    print "TOTAL TIME: ", total_time
    if total_time != 64:
        all_together_now()
    else:
        pass

    return entire_dance


if __name__ == "__main__":

    connect_to_db(app)
    print "Connected to DB."

    doctest.testmod(verbose=True)

    all_together_now()
