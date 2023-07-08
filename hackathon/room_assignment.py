import numpy as np
from time_assignment.create_similarity_matrix import create_similarity_matrix
from time_assignment.utils import read_csv
import networkx as nx

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

def assign_cluster_to_room(cluster_lst, room_info):
    '''
    Assigns clusters to rooms based on capacity.
    Creates a dict to keep track of what is where and how much space is left
    Assumes there to be enough space for all posters given as input
    '''
    count = 0
    while len(cluster_lst) > 0:
        cluster = cluster_lst.pop(0)
        check = False
        count_full = 0
        for idx,room in enumerate(room_info):
            free_space = room['poster_capacity'] - len(room_info[idx]['posters'])
            if free_space == 0:
                count_full += 1
                continue
            if len(cluster) <= free_space:
                print("cluster of {} posters assigned to room {}".format(len(cluster),room['name']))
                room_info[idx]['posters'] += cluster
                check = True
                break
        if count_full == len(room_info):
            raise ValueError('All rooms full! Too many posters!')
        if not check:
            print("cluster of {} posters could not be placed and will be split.".format(len(cluster)))
            split_idx = max(int(((len(cluster)-1)/2)),1)
            cluster_lst = [cluster[:split_idx]] + cluster_lst
            if len(cluster[split_idx:]) >= 0:
                cluster_lst = [cluster[split_idx:]] + cluster_lst
    return room_info

def get_room_info(graph_file):
   room_graph = nx.read_gml(graph_file)
   room_info = []
   room_data = [[node,data] for node,data in room_graph.nodes.data() if node.startswith('room')]
   for idx,room in enumerate(room_data):
      room_info.append({})
      room_info[idx]['ID'] = room[0]
      room_info[idx]['name'] = room[1]['room_name']
      room_info[idx]['poster_capacity'] = room[1]['n_posters']
      room_info[idx]['posters'] = []
   return room_info,room_graph

def flatten_sum(matrix):
    return sum(matrix, [])

def find_common_ones(i, A):
    i = int(i)
    posters = []
    n = np.shape(A)[0]
    for k in range(i+1,n):
        if (A[i][k]==1.0):
            posters.append(k)

    return posters

def fill_up_rooms(available_space_in_room, posters_in_room, A):
    added_posters = flatten_sum(posters_in_room)
    for room in range(len(available_space_in_room)):
        if (available_space_in_room[room] > 0):
            for poster in posters_in_room[room]:
                poster_ones = find_common_ones(poster,A)
                for ones in poster_ones:
                    if (available_space_in_room[room] > 0) and ones not in added_posters:
                        added_posters.append(ones)
                        posters_in_room[room].append(ones)
                        available_space_in_room[room]-=1
    missing_poster = []
    for i in range (np.shape(A)[0]):
        if i not in added_posters:
            missing_poster.append(i)

    for poster in missing_poster:
        for room in range(len(available_space_in_room)):
            while (available_space_in_room[room] > 0):
                added_posters.append(poster)
                posters_in_room[room].append(poster)
                available_space_in_room -= 1
            
    return posters_in_room, available_space_in_room            

def get_isolated_posters(n_poster,cluster_lst):
    poster_lst = np.arange(n_posters)
    for poster in poster_lst:
        check = False
        for cluster in cluster_lst:
            if not check and poster in cluster:
                check = True
        if not check:
            cluster_lst.append([poster])
    return cluster_lst

poster_data = read_csv("../sample_inputs/poster_data.csv")
similarity_matrix = create_similarity_matrix(poster_data)
poster_data = poster_data#[:50]
similarity_matrix = similarity_matrix#[:50,:50]
n_posters = similarity_matrix.shape[0]
matching_pairs = find_pairs(similarity_matrix)
cluster_lst = get_clusters(matching_pairs)
cluster_lst = get_isolated_posters(n_posters,cluster_lst)
if all_posters_used(cluster_lst,n_posters):
    print('Posters clustered successfully!')
room_graph_file = '../sample_inputs/graph_without_poster_assignment.gml'
room_info, room_graph = get_room_info(room_graph_file)
room_info = assign_cluster_to_room(cluster_lst,room_info)
#print(cluster_lst)

