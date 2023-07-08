import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

import csvreader as csv_reader

""" Script to generate the graph data from the actual hotel rooms via hardwired (for now) csv file """

input_file = '../data/relevant_rooms.csv'
relevant_metadata = ['length', 'width'  ]

room_data = csv_reader.extract_floor_plan(input_file)
## fill in the data
available_rooms = room_data['room'] 
room_metadata = []
for room in available_rooms:
  room_metadata.append( dict() )
  for key in relevant_metadata:
    room_metadata[-1][key] = room_data[key]

room_layout = nx.Graph()
room_layout.add_nodes_from( zip( room_data, room_metadata) )

