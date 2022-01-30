import pygame

import constants
import shared
from animsprite import AnimSprite
from .modeopening0 import ModeOpening0
from .modeopening import ModeOpening


class ModeCredits(ModeOpening):
    __slots__ = (
        '_time',
        '_background',
    )

    def __init__(self):
        super().__init__()
        self._time = 0
        self._background = pygame.Surface(constants.SCREEN_SIZE).convert(shared.display.screen)
        self._background.fill(constants.BLACK)
        # make an animsprite with rendered font for all credits
        # make it move to scroll

    def _switchMode(self):
        self.next_mode = ModeOpening0()

    def _update(self, dt):
        self._time += dt
        # after enough time for the credits to scroll, render text on to background
        # press any key to proceed etc

    def _drawScreen(self, screen):
        screen.blit(self._background, (0, 0))
