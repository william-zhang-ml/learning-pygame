"""
This module is the main module for the <title TBD> RPG game.
"""
import sys
import pygame
from levels import Level


WIDTH = 1600
HEIGHT = 900
FPS = 20


class Game:
    """ RPG game engine. """
    def __init__(self) -> None:
        """ Constructor. Setup. """
        # pylint: disable=no-member
        pygame.init()
        # pylint: enable=no-member
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()
        pygame.display.set_caption('RPG')

    def run(self) -> None:
        """ Start game engine. """
        # pylint: disable=no-member
        events = pygame.event.get()
        while all(e.type != pygame.QUIT for e in events):
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
            events = pygame.event.get()
        pygame.quit()
        # pylint: enable=no-member
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
