"""
This module implements the player asset.
"""
import pygame


SPEED = 10  # pixels per second


class Player(pygame.sprite.Sprite):
    """ Player asset for levels. """
    def __init__(self,
                 pos,
                 groups: pygame.sprite.Group,
                 obstacles: pygame.sprite.Group) -> None:
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
        """ Prevent player from moving through certain sprites. """
        if direction == 'horizontal':
            for sprite in self.obstacles:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacles:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom

    def move(self):
        """ Update player location in game. """
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.x += SPEED * self.direction.x
        self.handle_collision('horizontal')
        self.rect.y += SPEED * self.direction.y
        self.handle_collision('vertical')

    def update(self) -> None:
        """ Check user input for movement and move. """
        self.input()
        self.move()
