#!/usr/bin/env python
# -*- coding: utf-8 -*-

from networkx import read_gml
from networkx.readwrite import json_graph
import json
import os


def gml2json(gml_path):
    """Converts a gml file to a json file."""

    graph = read_gml(gml_path)
    converted_graph = json_graph.node_link_data(graph)

    path_without_ext = os.path.splitext(gml_path)[0]
    with open(f'{path_without_ext}.json', 'w') as fp:
        json.dump(converted_graph, fp, indent=4)


# example
if __name__ == "__main__":
    path = "../sample_inputs/graph_with_random_poster_assignment.gml"
    gml2json(path)
