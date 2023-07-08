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


def calc_timeslots(case: str, file: str = None, G: nx.graph = None):
    if case == "csv":
        # import data from csv
        if file == None:
            file = "sample_inputs/poster_data.csv"
        keywords = read_csv(file)
        slot_length = (len(keywords) - 1) // 4
        slot_sizes = [
            slot_length,
            slot_length,
            slot_length,
            len(keywords) - 1 - 3 * slot_length,
        ]
        # reduce data to only the columns we need
        keywords = keywords[1:, -3:]
        # first entry is new poster id
        keywords[:, 0] = np.arange(keywords.shape[0])

    else:
        # create mock graph
        if G == None:
            G = nx.read_gml("sample_inputs/graph_with_random_poster_assignment.gml")

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
    if case == "csv":
        keywords = np.concatenate((keywords, np.zeros((len(keywords), 1))), axis=1)
        keywords[0, -1] = "Timeslot"

    # call optimization
    best_assignments = random_optimization(
        matrix_distance, slot_sizes, neg_exp_loss, n_steps=100
    )  # 000)

    print(f"Best loss: {neg_exp_loss(matrix_distance, best_assignments)}")
    if case == "csv":
        keywords[1:, -1] = best_assignments
    else:
        for idx, best_val in enumerate(best_assignments):
            id_node = keywords[idx, 0]
            nodes_attrs[id_node]["timeslot"] = best_val

        nx.set_node_attributes(G, nodes_attrs)

    if case == "csv":
        write_csv(keywords, f"{file[:-4]}_plus_timeslot.csv")
    else:
        plot_graph_colored_time(G)


if __name__ == "__main__":
    case = "csv"
    calc_timeslots(case)
