from typing import List
import matplotlib.pyplot as plt

import numpy as np


def create_mock_data(n_samples: int):
    np.random.seed(1234)
    x = np.random.randn(n_samples, 3)
    theta = 3 * (x[:, 1] + 0.1 * x[:, 0])
    x = (0.2 * x[:, 2] + x[:, 1] + 2)[:, None] * np.stack([np.sin(theta), np.cos(theta)], axis=1)
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
        plt.plot(embeddings_2d[is_in_slot, 0], embeddings_2d[is_in_slot, 1], '.')

    plt.show()


if __name__ == '__main__':
    n_slots = 4
    slot_size = 30
    slot_sizes = [slot_size] * n_slots

    x = create_mock_data(n_slots * slot_size)
    dist_mat = compute_distance_matrix(x)
    assignments = random_assignments(slot_sizes)
    # print(f'{x=}')
    # print(f'{dist_mat=}')
    plot_assignments(x, assignments)