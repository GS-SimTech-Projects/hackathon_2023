from typing import Any, Callable, List

import numpy as np


class OptSpace:
    def sample_multi(self, n_samples: int) -> List[Any]:
        return [self.sample_single() for i in range(n_samples)]

    def sample(self) -> Any:
        raise NotImplementedError()

    def is_valid(self, value: Any) -> bool:
        raise NotImplementedError()

    def propose(self, value: Any) -> Any:
        raise NotImplementedError()

    def compute_loss(self, value: Any) -> float:
        raise NotImplementedError()

    def compute_loss_multi(self, values: List[Any]) -> List[float]:
        return [self.compute_loss(value) for value in values]


class TimeAssignmentOptSpace(OptSpace):
    def __init__(
        self,
        n_posters: int,
        min_slot_sizes: np.ndarray,
        max_slot_sizes: np.ndarray,
        allowed_slots: np.ndarray,
        loss_fn: Callable[[np.ndarray], float],
    ):
        # want to have multiple rooms with posters
        self.n_posters = n_posters
        self.min_slot_sizes = np.asarray(min_slot_sizes)
        self.max_slot_sizes = np.asarray(max_slot_sizes)
        self.allowed_slots = allowed_slots
        self.loss_fn = loss_fn

    def sample(self) -> Any:
        normalized_slot_sizes = (
            self.n_posters / np.sum(self.max_slot_sizes)
        ) * self.max_slot_sizes.astype(np.float64)
        cumsums = np.cumsum(normalized_slot_sizes).astype(np.int32)
        cumsums[-1] = self.n_posters
        cumsums = np.concatenate([[0], cumsums], axis=0)
        ref_slot_sizes = cumsums[1:] - cumsums[:-1]

        assignments = []
        for i, slot_size in enumerate(ref_slot_sizes):
            assignments.extend([i] * slot_size)
        assignments = np.array(assignments, dtype=np.int32)

        for i in range(1000):
            shuffled_assignments = assignments[np.random.permutation(len(assignments))]
            if self.is_valid(shuffled_assignments):
                return shuffled_assignments

        raise RuntimeError("No valid assignment found")

    def is_valid(self, value: Any) -> bool:
        raise NotImplementedError()

    def propose(self, value: Any) -> Any:
        raise NotImplementedError()

    def compute_loss(self, value: Any) -> float:
        raise NotImplementedError()


# class ProductOptSpace:
