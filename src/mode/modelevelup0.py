from collections import deque

import constants
import shared

import pygame

from .mode import Mode


class ModeLevelUp0(Mode):
    __slots__ = (
        'time',
        'background',
        'first_sprite',
        'sprite_switches',
    )

    def __init__(self):
        super().__init__()
        self.time = 0
        self.background = pygame.Surface(constants.SCREEN_SIZE).convert(shared.display.screen)
        self.background.fill(constants.WHITE)
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

        shared.state.protag_mon.visible = 0

        self.sprite_switches = deque((
            4000,
            4100,
            6000,
            6100,
            8000,
            8100,
            10000,
            10100,
            11000,
            11100,
            12000,
            12100,
            13000,
            13100,
            14000,
            14500,
            15000,
            15750,
            16000,
        ))
        # maybe text? could have no text though

    def _input(self, event):
        pass

    def _update(self, dt):
        self.time += dt
        while self.sprite_switches and self.time >= self.sprite_switches[0]:
            self._switchVisibleSprite()
            self.sprite_switches.popleft()

    def _switchVisibleSprite(self):
        if self.first_sprite.visible:
            self.first_sprite.visible = 0
            shared.state.protag_mon.visible = 1
        else:
            self.first_sprite.visible = 1
            shared.state.protag_mon.visible = 0

    def _drawScreen(self, screen):
        screen.blit(self.background, (0, 0))
