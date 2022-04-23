"""
This module implements moving and interacting entities.
"""
from typing import List
import pygame
from utils import load_graphics


SPEED = 20  # pixels per frame?
ANIMATION_SPEED = 0.25


class Entity(pygame.sprite.Sprite):
    """ General parent class for player, NPC, and monsters. """
    def __init__(self,
                 groups: List[pygame.sprite.Group]) -> None:
        """ Constructor.

        :param groups:    sprite groups containing this tile
        :type  groups:    List[pygame.sprite.Group]
        :param obstacles: group for sprites player cannot pass through
        :type  obstackes: pygame.sprite.Group
        """
        super().__init__(groups)
        self.frame_idx = 0
        self.is_attacking, self.attack_start_time = False, None
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


class Enemy(Entity):
    """ Interactable enemy implementation. """
    def __init__(self, pos, groups, species: str) -> None:
        """ Constructor.

        :param pos:       location of top-left corner in pixels (x, y)
        :type  pos:       Tuple[int, int]
        :param groups:    sprite groups containing this tile
        :type  groups:    List[pygame.sprite.Group]
        :param species:   monster species description (links to images)
        :type  species:   str
        """
        super().__init__(groups)

        # load enemy image assets
        self.image_lookup = {
            'attack': load_graphics(f'../graphics/monsters/{species}/attack'),
            'idle': load_graphics(f'../graphics/monsters/{species}/idle'),
            'move': load_graphics(f'../graphics/monsters/{species}/move')
        }

        if self.is_attacking:
            self.image = self.image_lookup['attack'][self.frame_idx]
        elif self.is_still:
            self.image = self.image_lookup['idle'][self.frame_idx]
        else:
            self.image = self.image_lookup['move'][self.frame_idx]
        self.rect = self.image.get_rect(topleft=pos)
