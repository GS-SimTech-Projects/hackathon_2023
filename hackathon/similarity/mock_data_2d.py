from typing import List

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def create_mock_graph():
    data = np.loadtxt(
        "sample_inputs/poster_data.csv", skiprows=1, dtype=str, delimiter=","
    )
    poster_names, keywords_1, keywords_2 = data[:, 0], data[:, 1], data[:, 2]
    n_posters = len(poster_names)

    G = nx.Graph()

    rooms = [
        ("room_00", {"pos": [0.0, 0.0], "room_name": "Stuttgart", "n_posters": 8}),
        ("room_01", {"pos": [0.0, 1.0], "room_name": "Bad Boll", "n_posters": 16}),
        ("room_02", {"pos": [1.0, -1.0], "room_name": "Muenchen", "n_posters": 8}),
        ("room_03", {"pos": [-1.0, -1.0], "room_name": "Foyer", "n_posters": 20}),
    ]

    hallways = [
        ("hw_00", {"pos": [0.0, -1.0]}),
    ]
    room_edges = [
        ("room_00", "room_01", {"distance": 1.0}),
    ]

    hallway_edges = [
        ("room_00", "hw_00", {"distance": 1.0}),
        ("room_02", "hw_00", {"distance": 1.0}),
        ("room_03", "hw_00", {"distance": 1.0}),
    ]

    posters = []
    poster_edges = []

    poster_counter = 0
    for room in rooms:
        for i in range(room[1]["n_posters"]):
            pos = room[1]["pos"] + np.random.uniform(-0.3, 0.3, size=2)
            distance = float(np.linalg.norm(room[1]["pos"] - pos))

            attrs = {
                "pos": (pos).tolist(),
                "name": "None",
                "kw_1": "None",
                "kw_2": "None",
                "timeslot": "None",
                "attendence": [],
            }
            poster = (f"poster_{poster_counter:03d}", attrs)
            posters.append(poster)
            poster_edges.append((room[0], poster[0], {"distance": distance}))
            poster_counter += 1

    G.add_nodes_from(rooms)
    G.add_nodes_from(posters)
    G.add_nodes_from(hallways)
    G.add_edges_from(room_edges)
    G.add_edges_from(poster_edges)
    G.add_edges_from(hallway_edges)

    return G


def create_mock_data(n_samples: int):
    np.random.seed(1234)
    x = np.random.randn(n_samples, 3)
    theta = 3 * (x[:, 1] + 0.1 * x[:, 0])
    x = (0.2 * x[:, 2] + x[:, 1] + 2)[:, None] * np.stack(
        [np.sin(theta), np.cos(theta)], axis=1
    )
    return x


def compute_distance_matrix(data: np.ndarray) -> np.ndarray:
    """
    Computes a matrix of distances.
    :param data: np.ndarray of shape [n_samples, dimension]
    :return: distance matrix of shape [n_samples, n_samples]
    """
    return np.linalg.norm(data[:, None, :] - data[None, :, :], axis=-1)


def random_assignments(slot_sizes: List[int]) -> np.ndarray:
    """
    Assigns posters randomly to slots
    :param slot_sizes: number of posters that should be assigned to a slot
    :return: a np.ndarray of type int such that result[poster_idx] = slot_id
    """
    assignments = []
    for i, slot_size in enumerate(slot_sizes):
        assignments.extend([i] * slot_size)
    assignments = np.array(assignments, dtype=np.int32)
    return assignments[np.random.permutation(len(assignments))]


def plot_assignments(embeddings_2d: np.ndarray, assignments: np.ndarray) -> None:
    """
    Plots 2d points and colors them according to their assignment
    :param embeddings_2d: np.ndarray of shape [n_points, 2]
    :param assignments: np.ndarray of shape [n_points]
    """
    n_slots = np.max(assignments) + 1
    plt.figure(figsize=(6, 4))

    for slot_idx in range(n_slots):
        is_in_slot = assignments == slot_idx
        plt.plot(embeddings_2d[is_in_slot, 0], embeddings_2d[is_in_slot, 1], ".")

    plt.show()


if __name__ == "__main__":
    n_slots = 4
    slot_size = 30
    slot_sizes = [slot_size] * n_slots

    x = create_mock_data(n_slots * slot_size)
    dist_mat = compute_distance_matrix(x)
    assignments = random_assignments(slot_sizes)
    # print(f'{x=}')
    # print(f'{dist_mat=}')
    plot_assignments(x, assignments)
