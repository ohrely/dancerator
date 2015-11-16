from model import connect_to_db, db
from app import app
import oopnow
import doctest


def make_dance():
    dance_moves, da_dict = oopnow.do_it_all()
    return dance_moves, da_dict


def count_star(dance, da_dict, i):
    total_moved = 1
    k = i - 1

    while k > 0:
        if da_dict[dance[k]].type_code == "star":
            total_moved += 1
            k -= 1
        else:
            k = 0

    star_count = "{} places".format(total_moved)

    return star_count


def simple_trans():
    """Translate dance code into readable choreography.
    """
    dance, da_dict = make_dance()
    translation = [[], [], [], []]

    i = 0
    beats = 0

    while i < len(dance):
        print da_dict[dance[i]].type_code
        if da_dict[dance[i]].type_code == da_dict[dance[i - 1]].type_code:
            if da_dict[dance[i]].type_code == "swing":
                move_name = ""
            elif da_dict[dance[i]].type_code == "star":
                try:
                    if da_dict[dance[i + 1]].type_code == "star":
                        move_name = ""
                    else:
                        move_name = count_star(dance, da_dict, i)
                except IndexError:
                    move_name = count_star(dance, da_dict, i)
            elif da_dict[dance[i]].type_code == "thru":
                move_name = da_dict[dance[i]].name + " again"
                return move_name
        else:
            move_name = da_dict[dance[i]].name

        if beats < 16:
            translation[0].append(move_name)
        elif beats < 32:
            translation[1].append(move_name)
        elif beats < 48:
            translation[2].append(move_name)
        elif beats < 64:
            translation[3].append(move_name)
        else:
            print "SOMETHING IS WRONG"

        # print translation
        beats = beats + da_dict[dance[i]].beats
        i += 1

    print translation
    return translation


if __name__ == "__main__":

    connect_to_db(app)
    print "Connected to DB."

    doctest.testmod(verbose=True)

    simple_trans()
