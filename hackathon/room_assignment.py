import numpy as np
from time_assignment.create_similarity_matrix import create_similarity_matrix
from time_assignment.utils import read_csv


def create_matrix(n):
    b = np.random.randint(0,2,size=(n,n))
    b_symm = (b + b.T)
    for i in range(n):
        b_symm[i][i] = 2
    return b_symm

def find_pairs(A):
    n = np.shape(A)[0]
    matching_pair = []
    print("n=",n)
    for row in range (n):
        print("row=",row)
        for column in range (row+1, n):
            print("column=",column)
            if (A[row][column]==2):
                print("matching pair", (row,column))
                matching_pair.append((row,column))
    return matching_pair


data = read_csv("../sample_inputs/poster_data.csv")
A = create_similarity_matrix(data)

print(A)
matching_pair = find_pairs(A)
print(matching_pair)