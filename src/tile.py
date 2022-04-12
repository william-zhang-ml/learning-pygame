"""
This module contains tile assets for constructing level maps.
"""
import pygame


class Tile(pygame.sprite.Sprite):
    """ Rock asset for levels. """
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
            pygame.image.load('../graphics/test/rock.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
