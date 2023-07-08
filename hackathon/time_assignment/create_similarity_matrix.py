import csv
import numpy as np
import os

def create_similarity_matrix(file:str = "sample_inputs/poster_data.csv"):
    # read csv file
    with open(file, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    # reduce data to only the columns we need
    # header = data[0]
    data = np.array(data[1:])
    data = data[:, -3:]
    data[:,0] = np.arange(data.shape[0])

def similarity(data1:np.ndarray, data2:np.ndarray):
    distance = 0
    for word in data1[1:]:
        if word in data2[1:]:
            distance += 1

    return distance

if __name__=="__main__":
    create_similarity_matrix()