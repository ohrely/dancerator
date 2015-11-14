from model import connect_to_db, db
from app import app
import oopnow
import doctest


def make_dance():
    dance_moves, da_dict = oopnow.do_it_all()
    return dance_moves, da_dict


def simple_trans():
    dance, da_dict = make_dance()
    # translation = [[], [], [], []]
    translation = []

    i = 0
    beats = 0

    while i < len(dance):
        if da_dict[dance[i]].type_code == da_dict[dance[i - 1]].type_code:
            if da_dict[dance[i]].type_code == "swing":
                move_name = ""
            elif da_dict[dance[i]].type_code == "star":
                if da_dict[dance[i + 1]].type_code == "star":
                    move_name = ""
                else:
                    total_moved = 0
                    k = i - 1
                    while k > 0:
                        if da_dict[dance[k]].type_code == "star":
                            total_moved += 1
                        else:
                            k = 0
                    move_name = "{} places".format(total_moved)
            elif da_dict[dance[i]].type_code == "thru":
                move_name = da_dict[dance[i]].name + " again"
        else:
            move_name = da_dict[dance[i]].name
        translation.append(move_name)
        beats = beats + da_dict[dance[i]].beats

    print translation
    return translation


if __name__ == "__main__":

    connect_to_db(app)
    print "Connected to DB."

    doctest.testmod(verbose=True)

    simple_trans()
