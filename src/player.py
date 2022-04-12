"""
This module contains the player asset.
"""
import pygame


class Player(pygame.sprite.Sprite):
    """ Player asset for levels. """
    def __init__(self,
                 pos,
                 groups: pygame.sprite.Group) -> None:
        """ Constructor.

        :param pos: _description_
        :type  pos: _type_
        :param groups: _description_
        :type  groups: _type_
        """
        super().__init__(groups)
        self.image = \
            pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
