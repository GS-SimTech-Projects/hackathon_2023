import numpy as np
from .utils import read_csv


def create_similarity_matrix(data: np.ndarray):
    # reduce data to only the columns we need
    # header = data[0]
    data = data[1:]
    data = data[:, -3:]
    data[:, 0] = np.arange(data.shape[0])

    matrix = np.zeros((data.shape[0], data.shape[0]))
    for i in range(data.shape[0]):
        for j in range(data.shape[0]):
            matrix[i, j] = similarity(data[i], data[j])
        assert matrix[i, i] == 2
    return matrix


def similarity(data1: np.ndarray, data2: np.ndarray):
    distance = 0
    for word in data1[1:]:
        if word in data2[1:]:
            distance += 1

    return distance


def test_matrix():
    data = read_csv()
    matrix = create_similarity_matrix(data)
    for i in range(data.shape[0] - 1):
        assert matrix[i, i] == 2, f"matrix values on diagonal should always be 2"


if __name__ == "__main__":
    data = read_csv()
    matrix = create_similarity_matrix(data)
    print(matrix)
    test_matrix()
