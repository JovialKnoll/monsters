import constants
import shared

import pygame

from .mode import Mode


class ModeLevelUp0(Mode):
    __slots__ = (
        'time',
        'first_sprite',
    )

    def __init__(self):
        super().__init__()
        self.time = 0
        shared.state.protag_mon.setImage(True)
        # set up first sprite
        self.first_sprite = pygame.sprite.DirtySprite()
        self.first_sprite.image = shared.state.protag_mon.image
        self.first_sprite.rect = shared.state.protag_mon.rect
        self.first_sprite.rect.midbottom = constants.SCREEN_CENTER
        # level up and set up second sprite
        shared.state.protag_mon.levelUp()
        shared.state.protag_mon.setImage(True)
        shared.state.protag_mon.rect.midbottom = constants.SCREEN_CENTER
        self.all_sprites.add(self.first_sprite, shared.state.protag_mon)

        self._setVisibleSprite(0)

        # save current sprite from monster, level it up, and flicker between them
        # maybe some special effects too
        # maybe text? could have no text though

    def _input(self, event):
        pass

    def _update(self, dt):
        self.time += dt
        if self.time >= 1000:
            self._setVisibleSprite(1)

    def _setVisibleSprite(self, index: int):
        self.first_sprite.visible = (index + 1) % 2
        shared.state.protag_mon.visible = index

    def _drawScreen(self, screen):
        screen.fill(constants.WHITE)
