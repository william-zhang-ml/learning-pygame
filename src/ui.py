"""
This module implements the user interface.
"""
import pygame
from player import Player


UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18
TEXT_COLOR = '#EEEEEE'

UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#EEEEEE'
UI_BORDER_HIGHLIGHT_COLOR = 'gold'

HEALTH_BOX = [10, 10, 200, 30]  # x, y, w, h
HEALTH_COLOR = 'red'

MANA_BOX = [10, 44, 150, 20]
MANA_COLOR = 'blue'

ITEM_BOX_SIZE = 80


class UserInterface:
    """ Visual elements that indirectly relate to gameplay (ex: healthbar). """
    def __init__(self) -> None:
        """ Constructor. """
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.health_bar = pygame.Rect(*HEALTH_BOX)
        self.mana_bar = pygame.Rect(*MANA_BOX)
        self.weapon_images = []
        for weap in ['sword', 'lance', 'axe', 'rapier', 'sai']:
            self.weapon_images.append(
                pygame.image.load(
                    f'../graphics/weapons/{weap}/full.png'
                ).convert_alpha()
            )

    def display_bar(self,
                    current: float,
                    limit: float,
                    color: str,
                    bg_rect: pygame.Rect) -> None:
        """ Display filled stat bars (ex: health). """
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # foreground size depends on stat value
        fg_rect = bg_rect.copy()
        fg_rect.width = bg_rect.width * current // limit
        pygame.draw.rect(self.display_surface, color, fg_rect)

        # border
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect, 3)

    def display_exp(self, exp: int) -> None:
        """ Display a rectangle w/num experience points in it.

            :param exp: number of experience points
            :type  exp: int
        """
        text = self.font.render(str(exp), False, TEXT_COLOR)
        rect = text.get_rect(bottomright=(
            self.display_surface.get_size()[0] - 40,
            self.display_surface.get_size()[1] - 40
        ))
        pygame.draw.rect(
            self.display_surface,
            UI_BG_COLOR,
            rect.inflate((20, 20))
        )
        pygame.draw.rect(
            self.display_surface,
            UI_BORDER_COLOR,
            rect.inflate(10, 10),
            2
        )
        self.display_surface.blit(text, rect)

    def display_weapon_box(self, player: Player) -> None:
        """ Display a rectangle that shows player's current weapons.

            :param player: the player
            :type  player: Player
        """
        bg_rect = pygame.Rect(20, 800, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        fg_weap = self.weapon_images[player.weapon_idx]
        self.display_surface.blit(
            fg_weap,
            fg_weap.get_rect(center=bg_rect.center)
        )
        if not player.can_change_weapon:
            pygame.draw.rect(
                self.display_surface,
                UI_BORDER_HIGHLIGHT_COLOR,
                bg_rect,
                3
            )

    def display(self, player: Player):
        """ Master UI update function. """
        self.display_bar(
            player.health,
            player.max_health,
            HEALTH_COLOR,
            self.health_bar)
        self.display_bar(
            player.mana,
            player.max_mana,
            MANA_COLOR,
            self.mana_bar)
        self.display_weapon_box(player)
        self.display_exp(player.exp)
