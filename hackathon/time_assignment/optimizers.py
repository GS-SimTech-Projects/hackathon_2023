from typing import Callable, List

import matplotlib.pyplot as plt
import numpy as np

from hackathon.similarity.mock_data_2d import (
    compute_distance_matrix,
    create_mock_data,
    plot_assignments,
    random_assignments,
)
from hackathon.time_assignment.loss_functions import (
    inv_dist_uneq_loss,
    neg_exp_loss,
    neg_exp_uneq_loss,
)


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

    # plt.figure()
    # plt.plot(np.arange(len(assignments_list)), scores)
    # plt.plot(best_scores)
    # plt.show()

    return assignments_list[np.argmin(scores)]


def local_optimization(
    dist_mat: np.ndarray,
    slot_sizes: List[int],
    loss_fn: Callable[[np.ndarray, np.ndarray], float],
    n_steps_initial: int = 10000,
    n_steps: int = 10000,
) -> np.ndarray:
    best_assignments = random_optimization(
        dist_mat, slot_sizes, loss_fn, n_steps=n_steps_initial
    )
    best_loss = loss_fn(dist_mat, best_assignments)
    start_loss = best_loss
    for i in range(n_steps):
        if i % 10 == 0:
            print(f"{i=}")
        idxs = np.random.choice(len(best_assignments), size=2, replace=False)
        proposal = np.copy(best_assignments)
        tmp = proposal[idxs[0]]
        proposal[idxs[0]] = proposal[idxs[1]]
        proposal[idxs[1]] = tmp
        proposal_loss = loss_fn(dist_mat, proposal)
        if proposal_loss < best_loss:
            best_loss = proposal_loss
            best_assignments = proposal

    print(f"Random optimizer score: {start_loss:g}")
    print(f"Best score after local optimization: {best_loss:g}")
    return best_assignments


def local_simulated_annealing_optimization(
    dist_mat: np.ndarray,
    slot_sizes: List[int],
    loss_fn: Callable[[np.ndarray, np.ndarray], float],
    n_steps_initial: int = 10000,
    n_steps: int = 10000,
    base_temp: float = 10.0,
) -> np.ndarray:
    best_assignments = random_optimization(
        dist_mat, slot_sizes, loss_fn, n_steps=n_steps_initial
    )
    best_loss = loss_fn(dist_mat, best_assignments)
    start_loss = best_loss
    for i in range(n_steps):
        temp = base_temp * np.exp(-5 * i / n_steps)
        if i % 10 == 0:
            print(f"{i=}")
        idxs = np.random.choice(len(best_assignments), size=2, replace=False)
        proposal = np.copy(best_assignments)
        tmp = proposal[idxs[0]]
        proposal[idxs[0]] = proposal[idxs[1]]
        proposal[idxs[1]] = tmp
        proposal_loss = loss_fn(dist_mat, proposal)
        u = np.random.rand()
        if np.exp(-(proposal_loss - best_loss) / temp) >= u:
            best_loss = proposal_loss
            best_assignments = proposal

    print(f"Random optimizer score: {start_loss:g}")
    print(f"Best score after local optimization: {best_loss:g}")
    return best_assignments


# basic functionality:
# have constraints - constraint checking
# random generation
# proposal generation


if __name__ == "__main__":
    n_slots = 4
    slot_size = 30
    slot_sizes = [slot_size] * n_slots
    # loss_fn = neg_exp_loss
    # loss_fn = lambda mat, assgn: neg_exp_loss(-mat, assgn)
    # loss_fn = lambda mat, assgn: -neg_exp_loss(-mat, assgn)
    loss_fn = neg_exp_uneq_loss
    # loss_fn = inv_dist_uneq_loss

    x = create_mock_data(n_slots * slot_size)
    dist_mat = 2.0 * compute_distance_matrix(x)

    # best_assignments = random_optimization(dist_mat, slot_sizes, loss_fn, n_steps=10000)
    best_assignments = local_optimization(
        dist_mat, slot_sizes, loss_fn, n_steps=100000, n_steps_initial=1000
    )
    # best_assignments = local_simulated_annealing_optimization(dist_mat, slot_sizes, loss_fn, n_steps=10000,
    #                                                           n_steps_initial=1000, base_temp=1000.0)
    print(f"Best loss: {loss_fn(dist_mat, best_assignments)}")
    plot_assignments(x, best_assignments)
