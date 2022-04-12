
"""
This module implements levels for the <title TBD> RPG game.
"""
import pygame


class Level:
    """ Level for RPG game. """
    def __init__(self) -> None:
        """ Constructor. """
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()   # can see on screen
        self.obstacle_sprites = pygame.sprite.Group()  # impede player movement

    def run(self) -> None:
        """ Load level into game. """
