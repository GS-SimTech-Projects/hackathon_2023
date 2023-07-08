import csv
from typing import List

import matplotlib.pyplot as plt
import numpy as np


def read_csv(file: str = "sample_inputs/poster_data.csv"):
    """
    Reads a csv file and returns a list of lists"""
    with open(file, newline="") as f:
        reader = csv.reader(f)
        data = list(reader)
    return np.array(data)
