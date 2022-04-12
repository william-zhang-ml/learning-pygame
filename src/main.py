"""
This module is the main module for the <title TBD> RPG game.
"""
import sys
import pygame


WIDTH = 1600
HEIGHT = 900
FPS = 20


class Game:
    """ RPG game engine. """
    def __init__(self) -> None:
        """ Constructor. Setup. """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

    def run(self) -> None:
        events = pygame.event.get()
        while all([e.type != pygame.QUIT for e in events]):
            self.screen.fill('black')
            pygame.display.update()
            self.clock.tick(FPS)
            events = pygame.event.get()

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
