import sys

import networkx as nx
import numpy as np

sys.path.append(
    "/home/pelzerja/Documents/Events/PhD_Retreat_2023/hackathon_2023/hackathon/similarity/"
)
sys.path.append(
    "/home/pelzerja/Documents/Events/PhD_Retreat_2023/hackathon_2023/hackathon/"
)
sys.path.append("/home/pelzerja/Documents/Events/PhD_Retreat_2023/hackathon_2023/")

from create_similarity_matrix import create_similarity_matrix
from loss_functions import neg_exp_loss
from optimizers import random_optimization
from utils import get_data_from_graph, plot_graph_colored_time, read_csv, write_csv


def calc_timeslots(file: str = None, G: nx.graph = None):
    # create mock graph
    if G == None:
        G = nx.read_gml(file)

    # get data from graph
    nodes_attrs, keywords = get_data_from_graph(G)
    slot_length = (len(keywords)) // 4
    slot_sizes = [
        slot_length,
        slot_length,
        slot_length,
        len(keywords) - 3 * slot_length,
    ]

    # create similarity matrix
    matrix_distance = create_similarity_matrix(
        keywords
    )  # expects data to have 3 inputs (id, kew1, kw2)

    # call optimization
    best_assignments = random_optimization(
        matrix_distance, slot_sizes, neg_exp_loss, n_steps=100
    )  # 000)

    print(f"Best loss: {neg_exp_loss(matrix_distance, best_assignments)}")
    for idx, best_val in enumerate(best_assignments):
        id_node = keywords[idx, 0]
        nodes_attrs[id_node]["timeslot"] = str(best_val)
        print(nodes_attrs[id_node]["timeslot"])

    nx.set_node_attributes(G, nodes_attrs)

    plot_graph_colored_time(G)
    nx.write_gml(G, f"{file[:-4]}_plus_timeslot.gml")


if __name__ == "__main__":
    graph_file = "sample_inputs/graph_with_random_poster_assignment.gml"
    calc_timeslots(graph_file)
