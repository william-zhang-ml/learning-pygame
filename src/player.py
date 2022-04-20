"""
This module implements the player asset.
"""
from typing import List, Tuple
import pygame
from utils import load_graphics


SPEED = 20  # pixels per second
CHANGE_WEAPON_COOLDOWN = 150
ATTACK_COOLDOWN = 100
ANIMATION_SPEED = 0.25
WEAPON_DATA = [
    {
        'type': 'sword',
        'cooldown': 100,
        'damage': 15,
        'graphic': '../graphics/weapons/sword/full.png'
    },
    {
        'type': 'lance',
        'cooldown': 400,
        'damage': 30,
        'graphic': '../graphics/weapons/lance/full.png'
    },
    {
        'type': 'axe',
        'cooldown': 300,
        'damage': 20,
        'graphic': '../graphics/weapons/axe/full.png'
    },
    {
        'type': 'rapier',
        'cooldown': 50,
        'damage': 8,
        'graphic': '../graphics/weapons/rapier/full.png'
    },
    {
        'type': 'sai',
        'cooldown': 80,
        'damage': 10,
        'graphic': '../graphics/weapons/sai/full.png'
    }
]
N_WEAPONS = len(WEAPON_DATA)


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
        self.health, self.max_health = 80, 100
        self.mana, self.max_mana = 50, 75
        self.exp = 420
        self.weapon_idx = 0
        self.can_change_weapon, self.change_weapon_time = True, 0
        self.is_attacking, self.attack_start_time = False, None
        # pylint: disable=c-extension-no-member
        self.facing = 'down'
        self.is_still, self.direction = True, pygame.math.Vector2()
        # pylint: enable=c-extension-no-member

        # set initial image to display
        self.frame_idx = 0
        self.image = self.image_lookup['down_idle'][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)  # pixels to add/sub
        self.weapon = None  # weapon sprite on screen

        # other
        self.obstacles = obstacles  # for collision handling

    def get_input(self) -> None:
        """ Get user input and update player status. """
        keys = pygame.key.get_pressed()

        # WEAPON CHANGE
        # pylint: disable=no-member
        if keys[pygame.K_q] and self.can_change_weapon:
            self.weapon_idx = (self.weapon_idx + 1) % N_WEAPONS
            self.can_change_weapon = False
            self.change_weapon_time = pygame.time.get_ticks()
        # pylint: enable=no-member

        # ATTACK
        # pylint: disable=no-member
        if keys[pygame.K_LSHIFT]:
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
            self.facing = 'up'
            self.direction.y = -1

        elif keys[pygame.K_DOWN]:
            self.facing = 'down'
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.facing = 'left'
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.facing = 'right'
            self.direction.x = 1
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
        self.can_change_weapon = \
            current_time - self.change_weapon_time > CHANGE_WEAPON_COOLDOWN

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

    def show_weapon(self) -> None:
        """ Create and show weapon sprite if player is attacking. """
        if self.weapon is not None:
            self.weapon.kill()
        if self.is_attacking:
            self.weapon = Weapon(self)

    def update(self) -> None:
        """ Check user input for movement and move. """
        self.get_input()
        self.apply_cooldown()
        self.set_image()
        self.move()
        self.show_weapon()


class Weapon(pygame.sprite.Sprite):
    """ Weapon asset. """
    def __init__(self, player: Player) -> None:
        """ Constructor.

            :param player: player that owns the weapon
            :type  player: Player
        """
        super().__init__(player.groups())
        weapon_type = WEAPON_DATA[player.weapon_idx]['type']
        self.image = pygame.image.load(
            f'../graphics/weapons/{weapon_type}/{player.facing}.png'
        ).convert_alpha()

        # offset placement away from player and adjust for player's sprite arm
        # pylint: disable=c-extension-no-member
        if player.facing == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright +
                                            pygame.math.Vector2(0, 16))
        elif player.facing == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft +
                                            pygame.math.Vector2(0, 16))
        elif player.facing == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom +
                                            pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midbottom=player.rect.midtop +
                                            pygame.math.Vector2(-10, 0))
        # pylint: enable=c-extension-no-member
