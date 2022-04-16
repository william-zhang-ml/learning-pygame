"""
This module implements custom sprite groups.
"""
import pygame


class CameraGroup(pygame.sprite.Group):
    """ Group to center game view on player sprite. """
    def __init__(self) -> None:
        """ Constructor. """
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        half_width, half_height = self.display_surface.get_size()
        half_width, half_height = half_width // 2, half_height // 2
        # pylint: disable=c-extension-no-member
        self.offset = pygame.math.Vector2()
        self.offset.x = half_width
        self.offset.y = half_height
        # pylint: enable=c-extension-no-member

        self.floor = \
            pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor.get_rect(topleft=(0, 0))

    def custom_draw(self, player: pygame.sprite.Sprite) -> None:
        """ Draw all group sprites relative to the player position.

            :param player: player sprite
            :type  player: pygame.sprite.Sprite
        """
        offset_from_player = [
            a - b
            for a, b in zip(self.floor_rect.topleft, player.rect.topleft)
        ]
        pos_on_screen = offset_from_player + self.offset
        self.display_surface.blit(self.floor, pos_on_screen)

        sorted_sprites = sorted(self.sprites(), key=lambda s: s.rect.centery)
        for sprite in sorted_sprites:  # inherited
            offset_from_player = [
                a - b
                for a, b in zip(sprite.rect.topleft, player.rect.topleft)
            ]
            pos_on_screen = offset_from_player + self.offset
            self.display_surface.blit(sprite.image, pos_on_screen)
