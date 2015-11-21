from model import connect_to_db, db
from model import Title
from random import sample
import algorithm
import doctest


def make_title():
    """Randmly generate a title for the dance using words from other dances' titles."""
    num_words = db.session.query(Title).count()
    word_ids = sample(xrange(num_words), 2)
    words_for_title = db.session.query(Title.word).filter(Title.word_id.in_(word_ids)).all()
    random_title = " ".join(word[0] for word in words_for_title)
    return random_title


def make_dance():
    """Generate dance."""
    dance_moves, da_dict = algorithm.do_it_all()
    return dance_moves, da_dict


def count_star(dance, da_dict, i):
    """Count number of places to move in one star figure.
    """
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
    print "DANCE IS ", dance

    i = 0
    beats = 0
    length = len(dance)

    while i < length:
        i_type = da_dict[dance[i]].type_code
        print da_dict[dance[i]].name
        if i < length - 1 and i_type == "hey" and da_dict[dance[i + 1]].type_code == "hey":
            move_name = "hey for four"
        elif da_dict[dance[i]].type_code == da_dict[dance[i - 1]].type_code:
            if da_dict[dance[i]].type_code in set(["swing", "hey"]):
                move_name = None
            elif da_dict[dance[i]].type_code == "star":
                try:
                    if da_dict[dance[i + 1]].type_code == "star":
                        move_name = None
                    else:
                        move_name = count_star(dance, da_dict, i)
                except IndexError:
                    move_name = count_star(dance, da_dict, i)
            elif da_dict[dance[i]].type_code == "thru":
                move_name = da_dict[dance[i]].name + " again"
            else:
                move_name = da_dict[dance[i]].name
        else:
            move_name = da_dict[dance[i]].name

        if move_name is not None:
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

        # for phrase in translation:
        #     if translation == []

        beats = beats + da_dict[dance[i]].beats
        i += 1

    print translation
    return translation


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print "Connected to DB."

    doctest.testmod(verbose=True)

    simple_trans()
    make_title()
