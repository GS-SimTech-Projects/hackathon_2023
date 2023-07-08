from typing import Callable, List

import matplotlib.pyplot as plt
import numpy as np

from hackathon.similarity.mock_data_2d import (
    compute_distance_matrix,
    create_mock_data,
    plot_assignments,
    random_assignments,
)
from hackathon.time_assignment.loss_functions import neg_exp_loss


def random_optimization(
    dist_mat: np.ndarray,
    slot_sizes: List[int],
    loss_fn: Callable[[np.ndarray, np.ndarray], float],
    n_steps: int = 1000,
) -> np.ndarray:
    assignments_list = []
    scores_list = []
    for i in range(n_steps):
        if i % 10 == 0:
            print(f"{i=}")
        assignments_list.append(random_assignments(slot_sizes=slot_sizes))
        scores_list.append(loss_fn(dist_mat, assignments_list[-1]))
    scores = np.array(scores_list)
    best_scores = [np.min(scores[: i + 1]) for i in range(len(scores))]

    plt.figure()
    plt.plot(np.arange(len(assignments_list)), scores)
    plt.plot(best_scores)
    plt.show()

    return assignments_list[np.argmin(scores)]


if __name__ == "__main__":
    n_slots = 4
    slot_size = 30
    slot_sizes = [slot_size] * n_slots
    loss_fn = neg_exp_loss

    x = create_mock_data(n_slots * slot_size)
    dist_mat = compute_distance_matrix(x)

    best_assignments = random_optimization(dist_mat, slot_sizes, loss_fn, n_steps=100000)
    print(f"Best loss: {loss_fn(dist_mat, best_assignments)}")
    plot_assignments(x, best_assignments)
