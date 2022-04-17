"""
This module implements the player asset.
"""
from typing import List, Tuple
import pygame
from utils import load_graphics


SPEED = 20  # pixels per second
ATTACK_COOLDOWN = 100
ANIMATION_SPEED = 0.25


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

        # load player image assets
        self.image_lookup = {}
        for player_state in [
            'up',
            'up_idle',
            'up_attack',
            'down',
            'down_idle',
            'down_attack',
            'left',
            'left_idle',
            'left_attack',
            'right',
            'right_idle',
            'right_attack'
        ]:
            self.image_lookup[player_state] = load_graphics(
                f'../graphics/player/{player_state}'
            )

        # set initial player status values
        self.is_attacking = False
        self.attack_start_time = None
        # pylint: disable=c-extension-no-member
        self.direction = pygame.math.Vector2()
        # pylint: enable=c-extension-no-member
        self.facing = 'down'
        self.is_still = True

        # set initial image to display
        self.frame_idx = 0
        self.image = self.image_lookup['down_idle'][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)  # pixels to add/sub

        # other
        self.obstacles = obstacles  # for collision handling

    def get_input(self) -> None:
        """ Get user input and update player status. """
        keys = pygame.key.get_pressed()

        # ATTACK
        # pylint: disable=no-member
        if keys[pygame.K_SPACE]:
            self.is_attacking = True
            self.attack_start_time = pygame.time.get_ticks()
        # pylint: enable=no-member

        # MAGIC
        # pylint: disable=no-member
        if keys[pygame.K_LCTRL]:
            self.is_attacking = True
            self.attack_start_time = pygame.time.get_ticks()
        # pylint: enable=no-member

        # MOVEMENT
        # pylint: disable=no-member
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.facing = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.facing = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing = 'right'
        else:
            self.direction.x = 0
        # pylint: enable=no-member
        self.is_still = self.direction.x == 0 and self.direction.y == 0

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

    def apply_cooldown(self) -> None:
        """ Check timers and update player status accordingly. """
        current_time = pygame.time.get_ticks()
        self.is_attacking = self.is_attacking and \
            current_time - self.attack_start_time < ATTACK_COOLDOWN

    def get_status_str(self) -> str:
        """ Create image lookup string from status info. """
        status = []
        status.append(self.facing)
        if self.is_attacking:
            status.append('attack')
        elif self.is_still:
            status.append('idle')
        return '_'.join(status)

    def set_image(self) -> None:
        """ Change sprite based on player status. """
        frames = self.image_lookup[self.get_status_str()]
        self.frame_idx = (self.frame_idx + ANIMATION_SPEED) % len(frames)
        self.image = frames[int(self.frame_idx)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

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
        self.get_input()
        self.apply_cooldown()
        self.set_image()
        self.move()
