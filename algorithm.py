# base case: total dance is 64 counts
# later base case: penultimate move flows into final move


class Move(object):
    def __init__(self, key=None, values=None, length=None):
        self.key = key
        self.values = values
        self.length = length

progression = # randomly chosen progression as tuple
first_move = progression[1]
last_move = progression[0]

DANCE_LENGTH = 64
len_left = DANCE_LENGTH - last_move.length

dance = []


def find_curr_values(key):
    # TODO query database for list of possible next keys
    # TODO return a randomly sorted list of those keys


# recursively build dance using a non-binary tree
def build_dance(curr_key, len_left, dance):

    # find out time left if current move were added to dance
    len_left = len_left - curr_key.length

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

    curr_values = find_curr_values(curr_key)

    # recursive call
    if len_left > 0:
        dance.append(curr_key)
        for next_key in curr_values:
            build_dance(next_key, len_left, dance)


print build_dance(first_move, len_left, dance)
