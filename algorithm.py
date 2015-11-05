# base case: total dance is 64 counts
# later base case: penultimate move flows into final move


class Move(object):
    def __init__(self, key=None, values=None, length=None):
        self.key = key
        self.values = values
        self.length = length


# progression = # randomly chosen progression as tuple
progression = ("llfb", "nswg")
first_move = progression[1]
last_move = progression[0]

DANCE_LENGTH = 64
len_left = DANCE_LENGTH - last_move.length

dance = []


def find_curr_values(key):
    """Return a randomly sorted list of possible next keys

    query database and randomly sort list of what comes back

    TODO doctest when there's a database
    """

# For testing - not real data
llfb = Move(llfb, pswg, 4)
pswg = Move(pswg, fchn, 8)

def build_dance(curr_key, len_left, dance):
    """Build 'legal' dance using recursion to ensure constraint satisfaction

    >>>build_dance(llfb, 8, [what, yass])
    [what, yass, llfb, pswg]

    """

    # find out time left if current move were added to dance
    len_left = len_left - curr_key.length
    curr_values = find_curr_values(curr_key)

    # fail condition
    if len_left < 0:
        print "too long"
        return

    # base case
    if len_left == 0:
        dance.append(curr_key)
        dance.append(last_move)
        return dance
        # TODO - ensure that this stops the function

    # recursive call
    if len_left > 0:
        dance.append(curr_key)
        for next_key in curr_values:
            build_dance(next_key, len_left, dance)

    return dance


print build_dance(first_move, len_left, dance)
