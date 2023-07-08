import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

import csvreader as csv_reader

""" Script to generate the graph data from the actual hotel rooms via hardwired (for now) csv file """

room_file = '../data/relevant_rooms.csv'
hallway_file = '../data/hallways.csv'
relevant_metadata = ['length', 'width']#, 'global_x', 'global_y' ]
connection_metadata = ['connects_to', 'connection_position' ]

def direct_distance( node1, node2):
    """
    compute the distance between two nodes given the 'pos' key in the node
    Parameters:
    -----------
    node1:      tuple of ('str', dict())
                tuple containing the node data, the dict must contain 'pos'
                'pos' may be a list or array of  two floats
    node2:      tuple of ('str', dict())
                tuple containing the node data, the dict must contain 'pos'
    Returns:
    --------
    distance:   list of three ints
                [direct_distance, x_distance, y_distance] 
    """
    distance_xy = [ abs(x-y) for x,y in zip( node1[-1]['pos'], node2[-1]['pos'] ) ]
    distance_diag = ( distance_xy[0]**2 + distance_xy[1]**2  ) **0.5
    return [distance_diag, *distance_xy]

room_data = csv_reader.extract_floor_plan( room_file)
hallway_data = csv_reader.extract_floor_plan( hallway_file)
## read the data of the graph and get zippable data
room_metadata = []
hallways = hallway_data['name']
rooms = room_data['room']
for i in range( len(rooms)):
    room_metadata.append( dict(room_name=rooms[i], has_poster=True) )
    for key in relevant_metadata:
        room_metadata[-1][key] = room_data.iloc[i][key] 
    room_metadata[-1]['pos'] = [room_data.iloc[i]['door_x'], room_data.iloc[i]['door_y']]
## add the hallways as rooms, may not contain posters
for i in range( len(hallways)):
    room_metadata.append( dict(room_name=hallways[i], has_poster=False) )
    room_metadata[-1]['pos'] = [room_data.iloc[i]['door_x'], room_data.iloc[i]['door_y']]
## room connectivity, each node may connect to multiple nodes
room_connections = []
for i in range( connections.shape[0] ): 
    room_connections.append( [connections[i,0], connections[i,1]] )
    room_connections[-1].append( dict( ) )
    for room in rooms:
      if not room == room_connections[-1][0]:
        continue
      else:
        for compare_room in rooms:
           if compare_room == room_connections[-1][1]: 
              full_distance = direct_distance( room['pos'], compareroom['pos'] )
              room_connections[-1]['distance'] = full_distance[0] 


room_layout = nx.Graph()
room_layout.add_nodes_from( zip( room_data['room'], room_metadata) )
room_layout.add_edges_from( room_connections)


