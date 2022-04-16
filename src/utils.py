"""
This module implements functions that are tangential to the core game engine.
"""
from typing import List
import os
from glob import glob
from csv import reader
import pygame


def load_map_layer(path: str) -> List[List[int]]:
    """ Load map layer stored in CSV file.

    :param path: path to map layer CSV file
    :type  path: str
    :return:     map layer
    :rtype:      List[List[int]]
    """
    with open(path, 'r', newline='\n', encoding='utf-8') as file:
        csvreader = reader(file, delimiter=',')
        layer = [[int(val) for val in line] for line in csvreader]
    return layer


def load_graphics(path: str) -> List[pygame.Surface]:
    """ Load PNG files in a directory (but not subdirectories) as surfaces.

    :param path: path to directory with PNG files
    :type  path: str
    :return:     loaded images
    :rtype:      List[pygame.Surface]
    """
    # pylint: disable=no-member
    assert pygame.display.get_surface() is not None, 'display not setup'
    # pylint: enable=no-member
    template = os.path.join(path, '*.png')
    return [
        pygame.image.load(image_file).convert_alpha()
        for image_file in glob(template)
    ]
