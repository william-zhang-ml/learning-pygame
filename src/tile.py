"""
This module implements tile assets for constructing level maps.
"""
from typing import List, Tuple
import pygame


TILE_SIZE = 64


class Tile(pygame.sprite.Sprite):
    """ Rock asset for levels. """
    def __init__(self,
                 pos: Tuple[int, int],
                 groups: List[pygame.sprite.Group],
                 sprite_type: str,
                 surface: pygame.Surface = None) -> None:
        """ Constructor.

        :param pos:         location of top-left corner in pixels (x, y)
        :type  pos:         Tuple[int, int]
        :param groups:      sprite groups containing this tile
        :type  groups:      List[pygame.sprite.Group]
        :param sprite_type: sprite type (visual)
        :type  sprite_type: str
        :param surface:     sprite image, defaults to block square
        :type  surface:     pygame.Surface, optional
        """
        super().__init__(groups)
        self.image = \
            surface or pygame.Surface((TILE_SIZE, TILE_SIZE))  # default
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)  # pixels to add/sub
        self.sprite_type = sprite_type
