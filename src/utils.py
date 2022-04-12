"""
This module implements functions that are tangential to the core game engine.
"""
from typing import List
from csv import reader


def load_map_layer(path: str) -> List[List[int]]:
    """ Load map layer stored in CSV file.

    :param path: path to mp layer CSV file
    :type  path: str
    :return:     map layer
    :rtype:      List[List[int]]
    """
    with open(path, 'r', newline='\n', encoding='utf-8') as file:
        csvreader = reader(file, delimiter=',')
        layer = [[int(val) for val in line] for line in csvreader]
    return layer
