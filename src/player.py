"""
This module implements the player asset.
"""
from typing import List, Tuple
import pygame


SPEED = 20  # pixels per second


class Player(pygame.sprite.Sprite):
    """ Player asset for levels. """
    def __init__(self,
                 pos: Tuple[int, int],
                 groups: List[pygame.sprite.Group],
                 obstacles: pygame.sprite.Group) -> None:
        """ Constructor.

        :param pos:       location of top-left corner in pixels (x, y)
        :type  pos:       Tuple[int, int]
        :param groups:    sprite groups containing this tile
        :type  groups:    List[pygame.sprite.Group]
        :param obstacles: group for sprites player cannot pass through
        :type  obstackes: pygame.sprite.Group
        """
        super().__init__(groups)
        self.image = \
            pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)  # pixels to add/sub
        # pylint: disable=c-extension-no-member
        self.direction = pygame.math.Vector2()
        # pylint: enable=c-extension-no-member
        self.obstacles = obstacles

    def input(self) -> None:
        """ Check for user input for movement. """
        keys = pygame.key.get_pressed()

        # pylint: disable=no-member
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        # pylint: enable=no-member

    def handle_collision(self, direction: str) -> None:
        """ Prevent player from moving through certain sprites.

            :param direction: direction in which to check collisions
            :type  direction: str
        """
        if direction == 'horizontal':
            for sprite in self.obstacles:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacles:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def move(self) -> None:
        """ Update player location in game. """
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += SPEED * self.direction.x
        self.handle_collision('horizontal')
        self.hitbox.y += SPEED * self.direction.y
        self.handle_collision('vertical')
        self.rect.center = self.hitbox.center

    def update(self) -> None:
        """ Check user input for movement and move. """
        self.input()
        self.move()
