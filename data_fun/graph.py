import networkx as nx
import matplotlib.pyplot as plt
from model import connect_to_db, db
from model import Move, Type_, Chain, Progression
import doctest


def make_graph():
    chain_graph = nx.DiGraph()

    all_moves = db.session.query(Move.move_code).all()

    chain_graph.add_nodes_from(all_moves)
    print "GRAPH HAS", chain_graph.number_of_nodes(), "NODES"

    all_chains = db.session.query(Chain.key_, Chain.value).all()

    chain_graph.add_edges_from(all_chains)
    print "GRAPH HAS", chain_graph.number_of_edges(), "EDGES"

    nx.draw(chain_graph)
    plt.savefig("graph.png")

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print "Connected to DB."

    doctest.testmod(verbose=True)

    make_graph()
