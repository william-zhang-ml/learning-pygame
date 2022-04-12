
"""
This module implements levels for the <title TBD> RPG game.
"""
import pygame
from tile import Tile
from player import Player
from group import CameraGroup
from utils import load_map_layer


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

    def create_map(self) -> None:
        """ Assign tiles to locations and sprite groups based on map nums. """
        layers = {
            'boundary': load_map_layer('../map/map_FloorBlocks.csv')
        }

        for _, layer in layers.items():
            for row_idx, row in enumerate(layer):
                for col_idx, val in enumerate(row):
                    x_pixel, y_pixel = TILE_SIZE * col_idx, TILE_SIZE * row_idx
                    if val == 395:
                        Tile(
                            (x_pixel, y_pixel),
                            [self.obstacle_sprites],
                            'invisible'
                        )

    def run(self) -> None:
        """ Load level into game. """
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
