
"""
This module implements levels for the <title TBD> RPG game.
"""
from random import choice
import pygame
from tile import Tile
from player import Player
from group import CameraGroup
from utils import load_map_layer, load_graphics


TILE_SIZE = 64


class Level:
    """ Level for RPG game. """
    def __init__(self) -> None:
        """ Constructor. """
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = CameraGroup()           # can see on screen
        self.obstacle_sprites = pygame.sprite.Group()  # impede player movement
        self.player = Player(
            (2000, 1430),
            [self.visible_sprites],
            self.obstacle_sprites
        )
        self.create_map()

    @staticmethod
    def load_layers() -> None:
        """ Loads and organizes level map assets. """
        return {
            'boundary': {
                'layout': load_map_layer('../map/map_FloorBlocks.csv'),
                'graphics': None,
                'val_to_graphic': lambda val, graphics: None,
                'groups': ('obstacle',)
            },
            'grass': {
                'layout': load_map_layer('../map/map_Grass.csv'),
                'graphics': load_graphics('../graphics/grass'),
                'val_to_graphic': lambda val, graphics: choice(graphics),
                'groups': ('visible', 'obstacle')
            },
            'object': {
                'layout': load_map_layer('../map/map_Objects.csv'),
                'graphics': load_graphics('../graphics/objects'),
                'val_to_graphic': lambda val, graphics: graphics[val],
                'groups': ('visible', 'obstacle')
            }
        }

    def create_map(self) -> None:
        """ Assign tiles to locations and sprite groups based on map nums. """
        str_to_group = {
            'visible': self.visible_sprites,
            'obstacle': self.obstacle_sprites
        }

        # define each tile in a level map layer in terms of its:
        # location, group membership, layer membership, graphic
        for layer_name, layer in self.load_layers().items():
            for row_idx, row in enumerate(layer['layout']):
                for col_idx, val in enumerate(row):
                    x_pixel, y_pixel = TILE_SIZE * col_idx, TILE_SIZE * row_idx
                    if val != -1:  # not whitespace
                        Tile(
                            (x_pixel, y_pixel),
                            [str_to_group[s] for s in layer['groups']],
                            layer_name,
                            layer['val_to_graphic'](val, layer['graphics'])
                        )

    def run(self) -> None:
        """ Load level into game. """
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
