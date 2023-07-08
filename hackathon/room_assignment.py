import numpy as np
from time_assignment.create_similarity_matrix import create_similarity_matrix
from time_assignment.utils import read_csv

def create_matrix(n):
    b = np.random.randint(0,2,size=(n,n))
    b_symm = (b + b.T)
    for i in range(n):
        b_symm[i][i] = 2
    return b_symm

def find_pairs(similarity_matrix):
    n = np.shape(similarity_matrix)[0]
    matching_pair = []
    for row in range (n):
        for column in range (row+1, n):
            if (similarity_matrix[row][column]==2):
                matching_pair.append(np.array([row,column]))
    return np.array(matching_pair)

def get_clusters(pair_lst):
    '''
    Creates clusters out of the pairs of posters with matching keywords, depth-first-search-style.
    This only creates one cluster per run, but goes through the pairs recursively until all
    posters have been clustered.
    '''
    binary_mask = np.array([True] * pair_lst.shape[0])
    cluster_lst = []
    cluster = []
    cluster += list(pair_lst[0])
    binary_mask[0] = False
    search_lst = []
    search_lst += list(pair_lst[0])
    while len(search_lst) > 0:
        entry = search_lst.pop(0)
        for idx,pair in enumerate(pair_lst):
            if not binary_mask[idx]:
                continue
            check = pair == entry
            if check.any():
                binary_mask[idx] = False
                to_be_added = list(pair[np.logical_not(check)])
                if not to_be_added in search_lst:
                    search_lst += to_be_added
                if not to_be_added in cluster:
                    cluster += to_be_added
    cluster_lst.append(cluster)
    if binary_mask.any(): # rescursion
        cluster_lst += get_clusters(pair_lst[binary_mask])
    return cluster_lst

def all_posters_used(cluster_lst,n_posters):
    '''
    Function to check if all posters are accounted for in one of the clusters
    '''
    poster_count = 0
    for cluster in cluster_lst:
        poster_count += len(cluster)
    if not  poster_count == n_posters:
        raise ValueError('Number of posters across all clusters does not match the number of posters that were read in from file! {} posters missing'.format(abs(poster_count - n_posters)))
    return True

def assign_cluster_to_room(cluster_lst, room_capacity):
    '''
    Assigns clusters to rooms based on capacity.
    Creates a dict to keep track of what is where and how much space is left
    '''
    placement = {}
    i = 0
    print(rooms)
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
    return

def get_room_graph(graph_file):
    

poster_data = read_csv("../sample_inputs/poster_data.csv")
similarity_matrix = create_similarity_matrix(poster_data)
n_posters = similarity_matrix.shape[0]
matching_pairs = find_pairs(similarity_matrix)
cluster_lst = get_clusters(matching_pairs)
if all_posters_used(cluster_lst,n_posters):
    print('Posters clustered successfully!')
room_graph_file = ''
room_graph = get_room_graph()
placement = assign_clusters_to room(cluster_lst,room_capacity)

