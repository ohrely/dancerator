# From algorithm.py.  Advantage of Move class: can easily query move attributes
# using methods.  Disadvantage: maybe none?  Might use later, but will need to
# change name b/c table querying is a thing.
class Move(object):
    def __init__(self, key=None, values=None, length=None):
        self.key = key
        self.values = values
        self.length = length

# Also from algorithm.py.  Intended for testing build_dance - not real data.
llfb = Move(llfb, pswg, 4)
pswg = Move(pswg, fchn, 8)
>>> build_dance(llfb, 8, [what, yass])
    [what, yass, llfb, pswg]


# In algorithm.py, at end of recursive call's for loop:
# TODO: is curr_values = curr_values[1:]  necessary? I don't think so.
