"""
This module implements tile assets for constructing level maps.
"""
from typing import List, Tuple
import pygame


class Tile(pygame.sprite.Sprite):
    """ Rock asset for levels. """
    def __init__(self,
                 pos: Tuple[int, int],
                 groups: List[pygame.sprite.Group]) -> None:
        """ Constructor.

        :param pos:    location of top-left corner in pixels (x, y)
        :type  pos:    Tuple[int, int]
        :param groups: sprite groups containing this tile
        :type  groups: List[pygame.sprite.Group]
        """
        super().__init__(groups)
        self.image = \
            pygame.image.load('../graphics/test/rock.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
