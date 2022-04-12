
"""
This module implements levels for the <title TBD> RPG game.
"""
import pygame
from tile import Tile
from player import Player
from group import CameraGroup


LEVEL_MAP = [
    list('xxxxxxxxxxxxxxxxxxxx'),
    list('x                  x'),
    list('x p                x'),
    list('x  x     xxxxx     x'),
    list('x  x         x     x'),
    list('x  x         x     x'),
    list('x  x         x     x'),
    list('x  x         x     x'),
    list('x  x         x     x'),
    list('x  x         x     x'),
    list('x  x         x     x'),
    list('x  x         xxx   x'),
    list('x      x x         x'),
    list('x     xxxxx        x'),
    list('x      xxx         x'),
    list('x       x          x'),
    list('x                  x'),
    list('x                  x'),
    list('x                  x'),
    list('xxxxxxxxxxxxxxxxxxxx')
]
TILE_SIZE = 64


class Level:
    """ Level for RPG game. """
    def __init__(self) -> None:
        """ Constructor. """
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = CameraGroup()           # can see on screen
        self.obstacle_sprites = pygame.sprite.Group()  # impede player movement
        self.player = None  # easy-access, often-used, assigned in create_map
        self.create_map()

    def create_map(self) -> None:
        """ Assign tiles to locations and sprite groups based on map chars. """
        for row_idx, row in enumerate(LEVEL_MAP):
            for col_idx, val in enumerate(row):
                x_pixel, y_pixel = TILE_SIZE * col_idx, TILE_SIZE * row_idx
                if val == 'x':
                    Tile(
                        (x_pixel, y_pixel),
                        [self.visible_sprites, self.obstacle_sprites]
                    )
                elif val == 'p':
                    self.player = Player(
                        (x_pixel, y_pixel),
                        [self.visible_sprites],
                        self.obstacle_sprites
                    )

    def run(self) -> None:
        """ Load level into game. """
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
