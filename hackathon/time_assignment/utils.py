import csv

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def read_csv(file: str = "sample_inputs/poster_data.csv"):
    """
    Reads a csv file and returns a list of lists
    """
    with open(file, newline="") as f:
        reader = csv.reader(f)
        data = list(reader)
    return np.array(data)


def write_csv(
    data: np.ndarray, file: str = "sample_inputs/poster_data_plus_timeslot.csv"
):
    """
    Writes a csv file and returns a list of lists
    """
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)


def get_data_from_graph(G: nx.graph):
    nodes = {}
    keywords = []
    for node in G.nodes:
        if node.startswith("poster"):
            nodes[node] = {
                "kw_1": G.nodes[node]["kw_1"],
                "kw_2": G.nodes[node]["kw_2"],
                "pos": G.nodes[node]["pos"],
                "name": G.nodes[node]["name"],
                "attendence": G.nodes[node]["attendence"],
                "timeslot": None,
            }
            keywords.append([node, G.nodes[node]["kw_1"], G.nodes[node]["kw_2"]])
    return nodes, np.array(keywords)


def plot_graph(G):
    room_nodes = [node for node in G.nodes if node.startswith("room")]
    poster_nodes = [node for node in G.nodes if node.startswith("poster")]
    hallway_nodes = [node for node in G.nodes if node.startswith("hw")]
    room_edges = [
        (u, v) for (u, v) in G.edges if u.startswith("room") and v.startswith("room")
    ]
    hallway_edges = [
        (u, v) for (u, v) in G.edges if u.startswith("hw") or v.startswith("hw")
    ]
    poster_edges = [
        (u, v) for (u, v) in G.edges if u.startswith("poster") or v.startswith("poster")
    ]

    pos = nx.get_node_attributes(G, "pos")
    room_labels = nx.get_node_attributes(G, "room_name")
    poster_labels = nx.get_node_attributes(G, "name")

    fig, ax = plt.subplots(figsize=(12, 12))
    nx.draw_networkx_nodes(
        G, pos, nodelist=poster_nodes, node_color="tab:blue", node_size=100
    )
    nx.draw_networkx_nodes(G, pos, nodelist=room_nodes, node_color="tab:red")
    nx.draw_networkx_nodes(G, pos, nodelist=hallway_nodes, node_color="tab:green")

    nx.draw_networkx_edges(G, pos, width=2.0, alpha=1.0, edgelist=room_edges)
    nx.draw_networkx_edges(G, pos, width=2.0, alpha=1.0, edgelist=hallway_edges)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, edgelist=poster_edges)

    nx.draw_networkx_labels(G, pos, labels=room_labels)
    nx.draw_networkx_labels(G, pos, labels=poster_labels)

    plt.show()


def plot_graph_colored_time(G):
    room_nodes = [node for node in G.nodes if node.startswith("room")]
    poster_nodes_time0 = [
        node
        for node, attrs in G.nodes(data=True)
        if node.startswith("poster") and (attrs["timeslot"] == 0)
    ]
    poster_nodes_time1 = [
        node
        for node, attrs in G.nodes(data=True)
        if node.startswith("poster") and (attrs["timeslot"] == 1)
    ]
    poster_nodes_time2 = [
        node
        for node, attrs in G.nodes(data=True)
        if node.startswith("poster") and (attrs["timeslot"] == 2)
    ]
    poster_nodes_time3 = [
        node
        for node, attrs in G.nodes(data=True)
        if node.startswith("poster") and (attrs["timeslot"] == 3)
    ]
    hallway_nodes = [node for node in G.nodes if node.startswith("hw")]
    room_edges = [
        (u, v) for (u, v) in G.edges if u.startswith("room") and v.startswith("room")
    ]
    hallway_edges = [
        (u, v) for (u, v) in G.edges if u.startswith("hw") or v.startswith("hw")
    ]
    poster_edges = [
        (u, v) for (u, v) in G.edges if u.startswith("poster") or v.startswith("poster")
    ]

    pos = nx.get_node_attributes(G, "pos")
    room_labels = nx.get_node_attributes(G, "room_name")
    poster_labels = nx.get_node_attributes(G, "name")

    fig, ax = plt.subplots(figsize=(12, 12))
    nx.draw_networkx_nodes(
        G, pos, nodelist=poster_nodes_time0, node_color="tab:blue", node_size=100
    )
    nx.draw_networkx_nodes(
        G, pos, nodelist=poster_nodes_time1, node_color="tab:orange", node_size=100
    )
    nx.draw_networkx_nodes(
        G, pos, nodelist=poster_nodes_time2, node_color="tab:green", node_size=100
    )
    nx.draw_networkx_nodes(
        G, pos, nodelist=poster_nodes_time3, node_color="tab:red", node_size=100
    )
    nx.draw_networkx_nodes(G, pos, nodelist=room_nodes, node_color="black")
    nx.draw_networkx_nodes(G, pos, nodelist=hallway_nodes, node_color="black")

    nx.draw_networkx_edges(G, pos, width=2.0, alpha=1.0, edgelist=room_edges)
    nx.draw_networkx_edges(G, pos, width=2.0, alpha=1.0, edgelist=hallway_edges)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, edgelist=poster_edges)

    nx.draw_networkx_labels(G, pos, labels=room_labels)
    nx.draw_networkx_labels(G, pos, labels=poster_labels)

    plt.show()
