import numpy as np


def neg_exp_loss(dist_mat: np.ndarray, assignments: np.ndarray) -> float:
    """
    Computes the loss \sum_{i, j} exp(-dist_{i, j}) * assigned_to_same(i, j)
    :param dist_mat: Distance matrix, shape [n_posters, n_posters]
    :param assignments: Assignment vector, assignments[poster_idx] = time_slot_idx, shape [n_posters]
    :return:
    """
    return np.sum(np.exp(-dist_mat) * (assignments[:, None] == assignments[None, :]))
