from typing import List
import pygame


SPEED = 20  # pixels per frame?
ANIMATION_SPEED = 0.25


class Entity(pygame.sprite.Sprite):
    """ General parent class for player, NPC, and monsters. """
    def __init__(self, groups: List[pygame.sprite.Group]) -> None:
        """ Constructor.

        :param groups:    sprite groups containing this tile
        :type  groups:    List[pygame.sprite.Group]
        :param obstacles: group for sprites player cannot pass through
        :type  obstackes: pygame.sprite.Group
        """
        super().__init__(groups)
        self.frame_idx = 0
        self.direction = pygame.math.Vector2()
        # pylint: disable=c-extension-no-member
        self.is_still, self.direction = True, pygame.math.Vector2()
        # pylint: enable=c-extension-no-member

    def handle_collision(self, direction: str) -> None:
        """ Prevent entity from moving through certain sprites.

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
