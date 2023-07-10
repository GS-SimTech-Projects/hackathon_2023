import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

import csvreader as csv_reader
from posterspacer import PosterSpacer

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
                    metadata from nodes which should be connected
    connect_to:     dict
                    metadata from the dictionary 
    Returns:
    --------
    edges:          list of [str,str,dict] pairs
                    edge data to be read as nx.Graph().add_edges_from
    """
    unknown_nodes = False
    for i in range( connections.shape[0] ): 
        room_connections.append( [connections.iloc[i,0], connections.iloc[i,1]] )
        room_connections[-1].append( dict( ) )
        room_connections[-1][-1]['distance'] = np.nan  #dict of the last entry 
        ## inefficient implementation via loops, simply find the corresponding rooms
        for room in connect_from:
          if not np.isnan( room_connections[-1][-1]['distance'] ):
              break
          if 'room_name' not in room:
              unknown_nodes = True
              continue
          if not room['room_name'] == room_connections[-1][0]:
              continue #if its not the room we're looking for
          else:
            ## find the connected room
            for connected_room in connect_to:
                if 'room_name' not in connected_room:
                  unknown_nodes = True 
                  continue
                if connected_room['room_name'] == room_connections[-1][1]: 
                  full_distance                    = direct_distance( room, connected_room )
                  room_connections[-1][-1]['distance'] = full_distance[0]  #dict of the last entry 
                  break 
    ## post processing, check if there were unconnected rooms
    uncoonected_rooms = False
    for connection in room_connections:
        if np.isnan( connection[-1]['distance']):
            unconnected_rooms = True 
    if unknown_nodes and unconnected_rooms:
        print( 'some nodes could not be connected')
        print( f'    because they are unknown: {unknown_nodes}' )
        print( '     make sure each node contains the "room_name" metadata')
    return room_connections

def get_posters( room_nodes):
    """
    Place the posters inside each 'room' given the arrangement inherited
    from the PosterSpacer and write the nodes for each poster
    The read datastructure is dependend on the PosterSpacer 
    and follows a very specific format
    Parameters:
    -----------
    room_nodes: list of ('room', dict( room_metadata) ) tuples
                room data which is in the node format for networkx
    Returns:
    --------
    room_posters:   list of list of ('poster_{}', dict( poster_metadata) )
                    consecutively numbered posters per room, from 0-n without
                    distinction between rooms
    poster_connectivities:  pandas.DataFrame
                            dataframe which indicates which poster belongs
                            to which room, follows the convention of the file
                            'data/connectivities.csv' (as of 2023, july, 10th)
                    
    """
    ctr = 0
    poster_connectivities = []
    poster_metadata = []
    room_posters = []
    for room, metadata in zip( rooms, room_metadata):
        local_posters = []
        floor = metadata['floor'] if 'floor' in metadata else None
        posters = PosterSpacer( 
            room_lower_left_corner_position=[metadata['global_x'],metadata['global_y'] ], 
            room_length=metadata['length_in_m'], room_width=metadata['length_in_m'] 
            )
        poster_positions = posters.get_poster_row_nodes()
        ## loop over all type of posters, and simply write all positions and allocate the rooms in a list
        for poster_block in poster_positions.values():
          for poster_row in poster_block.values():
            for position in poster_row:
              ctr += 1
              poster_identifier = f'poster_{ctr}'
              local_posters.append( [ poster_identifier, dict( room_name=poster_identifier, global_x=position[0], global_y=position[1], pos=position, floor=floor)] )
              poster_connectivities.append( dict( node=poster_identifier, connects_to=room ) )
              poster_metadata.extend( [x[-1] for x in local_posters] )
        room_posters.append( local_posters)
    ## list of dicts to dataframe
    poster_connectivities = pd.DataFrame( poster_connectivities)
    return room_posters, poster_metadata, poster_connectivities

def plot_graph( graph, floor=2, plot_labels=False): 
    """
    Plot the graph at the specified floor. Differentiates between hallway, room, and poster node
    finds the rooms via the metadata <has_poster=True>, hallways if the name contains 'hallway'
    detects posters if the name contains 'poster', so it might have been renamed when the 
    results of the poster group has been implemented
    Parameters:
    -----------
    graph:  networkx.Graph() object
            graph container for the room layout, each node must contain
            the metadata keywords 'pos=2tuple of ints' and 'floor=int'
    floor:  int, default 2
            which floor to plot
    plot_labels:    bool, default False
                    if the labels should be added on each node, functionality
                    can be surely improved, simply copied from the template (july10th 2023)
    Returns:
    --------
    fig, ax:    matplotlib.pyplot.subplots() figure objects
                plain plot containing the node data
    """
    room_nodes = []
    hallway_nodes = []
    poster_nodes = []
    for nodename, node_metadata in graph.nodes.data():
        if node_metadata['floor'] != floor:
            continue
        if 'has_poster' in node_metadata and node_metadata['has_poster']:
            room_nodes.append( nodename)
        if 'hallway' in nodename and node_metadata['floor'] == 2:
            hallway_nodes.append( nodename) 
        if 'poster' in nodename:
            poster_nodes.append( nodename)
    plotted_nodes = [*room_nodes, *hallway_nodes, *poster_nodes]
    global_connections = [(u,v) for (u,v) in graph.edges if u in plotted_nodes and v in plotted_nodes ] 
    pos = nx.get_node_attributes(graph,'pos')
    if plot_labels:
        room_labels = nx.get_node_attributes(graph,'room_name')
        poster_labels = nx.get_node_attributes(graph,'name') 
    fig, ax = plt.subplots(figsize=(12, 12))
    nx.draw_networkx_nodes(graph, pos, nodelist=poster_nodes, node_color="tab:blue", node_size=100, edgecolors='black')
    #nx.draw_networkx_nodes(graph, pos, nodelist=poster_nodes, node_color='blue', edgecolors='black' )
    nx.draw_networkx_nodes(graph, pos, nodelist=room_nodes, node_color="tab:red")
    nx.draw_networkx_nodes(graph, pos, nodelist=hallway_nodes, node_color="tab:green") 
    nx.draw_networkx_edges(graph, pos, width=2.0, alpha=1.0, edgelist=global_connections) 
    if plot_labels:
        nx.draw_networkx_labels(graph, pos, labels = room_labels)
        nx.draw_networkx_labels(graph, pos, labels = poster_labels)
    return fig, ax


if __name__ == '__main__':

    room_file           = '../data/relevant_rooms.csv'
    hallway_file        = '../data/hallways.csv'
    connection_file     = '../data/connections.csv'
    room_metakeys   = ['length_in_m', 'width_in_m', 'floor', 'global_x', 'global_y' ]
    hallway_metakeys = ['floor']

    room_data    = csv_reader.extract_floor_plan( room_file)
    hallway_data = csv_reader.extract_floor_plan( hallway_file)
    connections  = csv_reader.extract_floor_plan( connection_file)
    room_connections = []
    ## read the data of the graph and get zippable data
    rooms, room_metadata = read_nodes( 
            room_data, pos_idx=['door_x', 'door_y'], read_keys=room_metakeys, 
            global_metadata=dict(has_poster=True)
            )
    hallway, hallway_metadata = read_nodes( hallway_data, read_keys=hallway_metakeys, global_metadata=dict(has_poster=False))
    ## put all nodedata together to build the connections
    all_nodes = [ *rooms, *hallway ]
    all_metadata = [ *room_metadata, *hallway_metadata ]
    room_connections = get_edges( connections, hallway_metadata, all_metadata ) 
    #NOTE: here we use all_metadata as third argument because the hallways are interconnected, but rooms are not 
    ### extract the poster spaces for room
    room_posters, poster_metadata, poster_connectivities = get_posters( zip( rooms, room_metadata) )
    poster_connections = get_edges( poster_connectivities, poster_metadata, room_metadata ) 

    ### build the network graph
    room_layout = nx.Graph()
    room_layout.add_nodes_from( zip( all_nodes, all_metadata) )
    room_layout.add_edges_from( room_connections)
    for posters in room_posters:
        room_layout.add_nodes_from( posters) 
    room_layout.add_edges_from( poster_connections) 

    ## plot the graph
    fig, ax = plot_graph( room_layout, plot_labels=False)
    plt.show()
    ## save the graph
    ##nx.write_gml(room_layout, "../data/floor2_room+hallway+poster_layout.gml")
