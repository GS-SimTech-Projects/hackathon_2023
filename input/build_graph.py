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


room_file           = '../data/relevant_rooms.csv'
hallway_file        = '../data/hallways.csv'
connection_file     = '../data/connections.csv'
relevant_metadata   = ['length_in_m', 'width_in_m', 'floor']#, 'global_x', 'global_y' ]
connection_metadata = ['connects_to', 'connection_position' ]

room_data    = csv_reader.extract_floor_plan( room_file)
hallway_data = csv_reader.extract_floor_plan( hallway_file)
connections  = csv_reader.extract_floor_plan( connection_file)
## read the data of the graph and get zippable data
room_metadata    = []
hallways         = hallway_data['name']
rooms            = room_data['room']
room_connections = []
for i in range( len(rooms)):
    room_metadata.append( dict(room_name=rooms[i], has_poster=True) )
    for key in relevant_metadata:
        if key in room_data.iloc[i]:
            room_metadata[-1][key] = room_data.iloc[i][key] 
    room_metadata[-1]['pos'] = [room_data.iloc[i]['door_x'], room_data.iloc[i]['door_y']]
## add the hallways as rooms, may not contain posters
for i in range( len(hallways)):
    room_metadata.append( dict(room_name=hallways[i], has_poster=False) )
    for key in relevant_metadata:
        if key in hallway_data.iloc[i]:
            room_metadata[-1][key] = hallway_data.iloc[i][key] 
    room_metadata[-1]['pos'] = [hallway_data.iloc[i]['global_x'], hallway_data.iloc[i]['global_y']]
room_names = [ *rooms, *hallways]
## room connectivity, each node may connect to multiple nodes
for i in range( connections.shape[0] ): 
    room_connections.append( [connections.iloc[i,0], connections.iloc[i,1]] )
    room_connections[-1].append( dict( ) )
    for room in room_metadata:
      if not room['room_name'] == room_connections[-1][0]:
        continue
      else:
        for compare_room in room_metadata:
           if compare_room['room_name'] == room_connections[-1][1]: 
              full_distance                    = direct_distance( room, compare_room )
              room_connections[-1][-1]['distance'] = full_distance[0] 



room_layout = nx.Graph()
room_layout.add_nodes_from( zip( room_names, room_metadata) )
room_layout.add_edges_from( room_connections)

#def plot_graph(G): 
G = room_layout
if True:
    room_nodes = []
    hallway_nodes = []
    for nodename, node_metadata in G.nodes.data():
        if 'has_poster' in node_metadata and node_metadata['has_poster']:
            print( 'adding node to the room notes' )
            room_nodes.append( nodename)
        if 'hallway' in nodename and node_metadata['floor'] == 2:
            hallway_nodes.append( nodename) 
    plotted_nodes = [*room_nodes, *hallway_nodes]

    #room_edges = [(u,v) for (u,v) in G.edges if u.startswith("room") and v.startswith("room")]
    global_connections = [(u,v) for (u,v) in G.edges if u in plotted_nodes and v in plotted_nodes ]
    print( global_connections)
    #hallway_edges = [(u,v) for (u,v) in G.edges if u.startswith("hw") or v.startswith("hw")]
    #poster_edges = [(u,v) for (u,v) in G.edges if u.startswith("poster") or v.startswith("poster")]

    pos=nx.get_node_attributes(G,'pos')
    room_labels = nx.get_node_attributes(G,'room_name')
    poster_labels = nx.get_node_attributes(G,'name')

    fig, ax = plt.subplots(figsize=(12, 12))
    #nx.draw_networkx_nodes(G, pos, nodelist=poster_nodes, node_color="tab:blue", node_size=100)
    nx.draw_networkx_nodes(G, pos, nodelist=room_nodes, node_color="tab:red")
    nx.draw_networkx_nodes(G, pos, nodelist=hallway_nodes, node_color="tab:green")

    nx.draw_networkx_edges(G, pos, width=2.0, alpha=1.0, edgelist=global_connections)
    ###nx.draw_networkx_edges(G, pos, width=2.0, alpha=1.0, edgelist=room_edges)
    ###nx.draw_networkx_edges(G, pos, width=2.0, alpha=1.0, edgelist=hallway_edges)
    ###nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, edgelist=poster_edges)

    #nx.draw_networkx_labels(G, pos, labels = room_labels)
    #nx.draw_networkx_labels(G, pos, labels = poster_labels)


#plot_graph( room_layout)
plt.show()
