from model import Move, Type_, Chain, Progression
from model import connect_to_db, db
from server import app
import doctest


# seed types to Types
def add_types():
    """Seed types from _____ to database"""

    print("Types")

    Type_.query.delete()

    # for row in open("seed_data/types.txt"):
    #     row = row.rstrip()
    #     row = row.split(",")
    #     type_code = row[0]
    #     min_repeats = row[1]
    #     max_repeats = row[2]
    #     print(type_code, min_repeats, max_repeats)

    #     type_ = Type_(type_code=type_code,
    #                   min_repeats=min_repeats,
    #                   max_repeats=max_repeats)

    #     db.session.add(type_)

    # db.session.commit()


# # seed moves to Moves
def add_moves():
    """Seed moves from _____ to database"""

    print("Moves")

    Move.query.delete()


# # PSEUDOCODE FOR SEEDING PROGRESSIONS AND CHAINS
# def parse_csv(dance_data):
#     """
#     >>> parse_csv("seed_data/dances.txt")[-1]
#     ['ngrm', 'nswg', 'nswg', 'llfb', 'lal6', 'pbal', 'pswg', 'pswg', 'pswg', 'pprm', 'crl3*']
#     """
#     dance_list = []
#     # TODO consider addressing * at end of some dances
#     for dance in (open(dance_data)):
#         dance = dance.split(",")
#         dance = dance[2]
#         dance = dance.replace("|", "")
#         dance = dance.rstrip()
#         dance = dance.split()
#         dance_list.append(dance)

#     return dance_list

# dances = parse_csv("seed_data/dances.txt")

# def seed_prog(dance):
#     """Takes dance as a list of moves and seeds Progressions table.

#     """
#     last = dance[-1]
#     first = dance[0]

#     # if last, first in Progressions:
#     #     pass
#     # else:
#     #     add last, first to Progressions

# def seed_chains(dance):
#     """Takes dance as a list of moves and seeds Chains table.

#     """
#     last = dance[-1]
#     first = dance[0]

#     i = 0
#     while i < (len(dance)-1):
#         key = dance[i]
#         value = dance[i+1]
#         # if key, value in Chains:
#         #     pass
#         # else:
#         #     add key, value to Chains
#         i += 1

# def seed_dances(dances):
#     """Seed data from dances into Progressions and Chains tables.

#     Ensures that both processes are seeded when data is passed in.

#     TODO add tests!
#     """
#     for dance in dances:
#         seed_prog(dance)
#         seed_chains(dance)


# seed_dances(dances)


if __name__ == "__main__":
    doctest.testmod(verbose=True)

    add_types()
