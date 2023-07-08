import numpy as np
from pandas_ods_reader import read_ods

def get_data(path):
    data = read_ods(path)
    return data

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

input_file = '../data/poster_registrations.ods'
data = get_data(input_file)
print(data)
n = 6
A = create_matrix(n)
print(A)
matching_pair = find_pairs(A)
print(matching_pair)

#TODO
# place one poster
# check this posters score with all the others
# do a ranking
# build a cluster with maximum score
#   first take all the score two
#   then take score ones to fill up, if there are spots left
