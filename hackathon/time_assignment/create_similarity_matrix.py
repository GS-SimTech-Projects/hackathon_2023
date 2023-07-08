import numpy as np
from utils import read_csv


def create_similarity_matrix(data: np.ndarray):
    """
    :param data: numpy array of shape (n, columns) where n is the number of rows (posters) in the csv file
    :return: matrix as numpy array of shape (n, n) where n is the number of rows (posters) in the csv file
    """
    # reduce data to only the columns we need
    data = data[1:]
    data = data[:, -3:]
    # first entry is new poster id
    data[:, 0] = np.arange(data.shape[0])

    matrix = np.zeros((data.shape[0], data.shape[0]))
    for i in range(data.shape[0]):
        for j in range(data.shape[0]):
            matrix[i, j] = similarity(data[i], data[j])
        assert matrix[i, i] == 2
    return matrix


def similarity(data1: np.ndarray, data2: np.ndarray):
    """
    returns similarity between two data points (posters)
    :param data1: numpy array of shape (3,) with first entry: index, second and third entry: keywords
    :param data2: numpy array of shape (3,) with first entry: index, second and third entry: keywords
    :return: similarity between data1 and data2
    """
    distance = 0
    for word in data1[1:]:
        if word in data2[1:]:
            distance += 1

    return distance


def test_matrix():
    """
    test if the value on the diagonal is always 2 otherwise assert
    """
    data = read_csv()
    matrix = create_similarity_matrix(data)
    for i in range(data.shape[0] - 1):
        assert matrix[i, i] == 2, f"matrix values on diagonal should always be 2"


if __name__ == "__main__":
    data = read_csv()
    matrix = create_similarity_matrix(data)
    print(matrix)
    test_matrix()
