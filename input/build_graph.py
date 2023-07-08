import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

import csvreader as csv_reader

""" Script to generate the graph data from the actual hotel rooms via hardwired (for now) csv file """

def direct_distance( node1, node2):
    """
    compute the distance between two nodes given the 'pos' key in the node
    metadata, before graph creation
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
    distance_xy   = [ abs(x-y) for x,y in zip( node1['pos'], node2['pos'] ) ]
    distance_diag = ( distance_xy[0]**2 + distance_xy[1]**2  ) **0.5
    return [distance_diag, *distance_xy]

def read_nodes( data_structure, pos_idx=['global_x','global_y'], read_keys=dict(), global_metadata=dict() ):
    """
    Read the nodes from a pandas dataframe. The nodes are either given
    by 'name' or 'room', and must contain information about the position
    (preferrably global).
    Parameters:
    -----------
    data_structure:     pandas.DataFrame
                        data container of the rooms/hallways
    pos_idx:            list of str, default ['global_x', 'global_y']
                        identifier to the position variable within the csv file
    read_keys:          dict, default ()
                        metadata that should be read from the file and copied
                        to the node structure (under the same key)
    global_metadata:    dict, default ()
                        metadata that should be added to every node in 
                        the datastructure, e.g. dict( has_poster=True) 
    Returns:    
    --------    
    nodes:      [list of (tuples with str, dict)]
    """
    metadata = []
    rooms = data_structure['name'] if 'name' in data_structure else data_structure['room']
    for i in range( len(rooms)):
        metadata.append( dict(room_name=rooms[i], **global_metadata) )
        for key in read_keys:
            if key in data_structure.iloc[i]:
                metadata[-1][key] = data_structure.iloc[i][key] 
        metadata[-1]['pos'] = [data_structure.iloc[i][pos_idx[0]], data_structure.iloc[i][pos_idx[1]]]
    return rooms, metadata

def get_edges( connections, connect_from, connect_to ):
    """
    get the edge connections list of multiple [ node1, node2, dict( distance=d) ]
    pairs. May be the same, i.e. 'all_metadata' if there are interconnections
    Parameters:
    -----------
    connections:    pandas dataframe 
                    containing 'node', 'connect_to'  entries
    connect_from:   dict
                    metadata from the dictionary 
    connect_to:     dict
                    metadata from the dictionary 
    Returns:
    --------
    edges:          list of [str,str,dict] pairs
                    edge data to be read as nx.Graph().add_edges_from
    """
    for i in range( connections.shape[0] ): 
        room_connections.append( [connections.iloc[i,0], connections.iloc[i,1]] )
        room_connections[-1].append( dict( ) )
        for room in connect_from:
          if not room['room_name'] == room_connections[-1][0]:
            continue
          else:
            for compare_room in connect_to:
               if compare_room['room_name'] == room_connections[-1][1]: 
                  full_distance                    = direct_distance( room, compare_room )
                  room_connections[-1][-1]['distance'] = full_distance[0] 
    return room_connections



room_file           = '../data/relevant_rooms.csv'
hallway_file        = '../data/hallways.csv'
connection_file     = '../data/connections.csv'
room_metakeys   = ['length_in_m', 'width_in_m', 'floor']#, 'global_x', 'global_y' ]
hallway_metakeys = ['floor']

room_data    = csv_reader.extract_floor_plan( room_file)
hallway_data = csv_reader.extract_floor_plan( hallway_file)
connections  = csv_reader.extract_floor_plan( connection_file)
room_connections = []
## read the data of the graph and get zippable data
rooms, room_metadata = read_nodes( room_data, pos_idx=['door_x', 'door_y'], read_keys=room_metakeys, global_metadata=dict(has_poster=True))
hallway, hallway_metadata = read_nodes( hallway_data, read_keys=hallway_metakeys, global_metadata=dict(has_poster=False))
all_nodes = [ *rooms, *hallway ]
all_metadata = [ *room_metadata, *hallway_metadata ]
room_connections = get_edges( connections, hallway_metadata, all_metadata) #NOTE: here we use all_metadata as third argument because the hallways are interconnected, but rooms are not
room_layout = nx.Graph()
room_layout.add_nodes_from( zip( all_nodes, all_metadata) )
room_layout.add_edges_from( room_connections)


#def plot_graph(room_layout): 
room_layout = room_layout
## this plotting function should be modularized, ultimately it only takes the room_nodes as input so its ez, but honestly its wayyy too late and im way too unmotivated
if True:
    room_nodes = []
    hallway_nodes = []
    for nodename, node_metadata in room_layout.nodes.data():
        if 'has_poster' in node_metadata and node_metadata['has_poster']:
            room_nodes.append( nodename)
        if 'hallway' in nodename and node_metadata['floor'] == 2:
            hallway_nodes.append( nodename) 
    plotted_nodes = [*room_nodes, *hallway_nodes]
    global_connections = [(u,v) for (u,v) in room_layout.edges if u in plotted_nodes and v in plotted_nodes ] 
    pos=nx.get_node_attributes(room_layout,'pos')
    room_labels = nx.get_node_attributes(room_layout,'room_name')
    poster_labels = nx.get_node_attributes(room_layout,'name') 
    fig, ax = plt.subplots(figsize=(12, 12))
    #nx.draw_networkx_nodes(room_layout, pos, nodelist=poster_nodes, node_color="tab:blue", node_size=100)
    nx.draw_networkx_nodes(room_layout, pos, nodelist=room_nodes, node_color="tab:red")
    nx.draw_networkx_nodes(room_layout, pos, nodelist=hallway_nodes, node_color="tab:green") 
    nx.draw_networkx_edges(room_layout, pos, width=2.0, alpha=1.0, edgelist=global_connections) 
    #nx.draw_networkx_labels(room_layout, pos, labels = room_labels)
    #nx.draw_networkx_labels(room_layout, pos, labels = poster_labels)

plt.show()
