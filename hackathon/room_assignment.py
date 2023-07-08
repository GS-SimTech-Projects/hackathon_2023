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


def assign_cluster_to_room(clusters, rooms):
    #assume rooms are ordered from more to less poster space
    #assume clusters are ordered from more to less poster space
    i = 0
    while (i < len(clusters)):
        for k in range(len(rooms)):
            if clusters[i]<=rooms[k]:
                print("cluster of %d posters assigned to room %d" %(clusters[i],k+1))
                rooms[k]=rooms[k]-clusters[i]
                break
            if (k==len(rooms)-1):
                print("cluster of %d posters could not be placed." %(clusters[i]))

                clusters.append(np.ceil(clusters[i]/2))
                clusters.append(np.floor(clusters[i]/2))
                break
        i+=1

# clusters = [7,5,4,3]
# rooms = [12, 6, 2]

# assign_cluster_to_room(clusters,rooms)

# data = read_csv("../sample_inputs/poster_data.csv")
# A = create_similarity_matrix(data)

# print(A)
# matching_pair = find_pairs(A)
# print(matching_pair)

#TODO
# place one poster
# check this posters score with all the others
# do a ranking
# build a cluster with maximum score
#   first take all the score two
#   then take score ones to fill up, if there are spots left

A = np.eye(3)
A[1,2] = 2.0
print(A)
matching_pair=find_pairs(A)
print(matching_pair)
assign_clusters(matching_pair)