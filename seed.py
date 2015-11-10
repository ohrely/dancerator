from model import Move, Type_, Chain, Progression
from model import connect_to_db, db
from server import app
import doctest


def add_types(type_data):
    """Seed types from csv to database"""

    print("Types")

    Type_.query.delete()

    for row in open(type_data):
        row = row.rstrip()
        row = row.split(",")
        type_code = row[0]
        min_repeats = row[1]
        max_repeats = row[2]

        type_ = Type_(type_code=type_code,
                      min_repeats=min_repeats,
                      max_repeats=max_repeats)

        db.session.add(type_)

    db.session.commit()


def add_moves(move_data):
    """Seed moves from csv to database"""

    print("Moves")

    Move.query.delete()

    for row in open(move_data):
        row = row.rstrip()
        row = row.split(",")
        move_code = row[0]
        type_code = row[1]
        move_name = row[2]
        beats = row[3]

        move = Move(move_code=move_code,
                    type_code=type_code,
                    move_name=move_name,
                    beats=beats)

        db.session.add(move)

    db.session.commit()


def parse_csv(dance_data):
    """Parse csv (from Google Sheets).

    >>> parse_csv("seed_data/dances.txt")[-1]
    ['ngrm', 'nswg', 'nswg', 'llfb', 'lal6', 'pbal', 'pswg', 'pswg', 'pswg', 'pprm', 'crl3']
    """
    dance_list = []

    for row in (open(dance_data)):
        row = row.split(",")
        dance = row[2]
        dance = dance.replace("|", "")
        dance = dance.rstrip()
        dance = dance.split()
        dance_list.append(dance)

    return dance_list


def seed_prog(dance):
    """Takes dance as a list of moves and seeds Progressions table.

    """
    print("Progressions")

    last = dance[-1]
    first = dance[0]

    try:
        db.session.query(Progression).filter_by(last=last, first=first).one()
    except:
        progression = Progression(last=last, first=first)

        db.session.add(progression)
        db.session.commit()


def seed_chains(dance):
    """Takes dance as a list of moves and seeds Chains table.

    """
    print("Chains")

    i = 0
    while i < (len(dance)-1):
        key_ = dance[i]
        value = dance[i+1]

        try:
            db.session.query(Chain).filter_by(key_=key_, value=value).one()
        except:
            chain = Chain(key_=key_, value=value)

            db.session.add(chain)
            db.session.commit()

        i += 1


def seed_dances(dance_file):
    """Seed data from dances into Progressions and Chains tables.

    Ensures that both processes are seeded when data is passed in.

    TODO add tests!
    """
    Progression.query.delete()
    Chain.query.delete()

    dances = parse_csv(dance_file)

    for dance in dances:
        seed_prog(dance)
        seed_chains(dance)


if __name__ == "__main__":
    connect_to_db(app)

    doctest.testmod(verbose=True)

    add_types("seed_data/types.txt")
    add_moves("seed_data/moves.txt")
    seed_dances("seed_data/dances.txt")
