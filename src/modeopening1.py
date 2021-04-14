import pygame

import constants
import shared
from mode import Mode
from modeopening2 import ModeOpening2
from animsprite import AnimSprite

class ModeOpening1(Mode):
    logo_text = "tinsil"

    __slots__ = (
        'time',
        'step',
        'background',
    )

    def __init__(self):
        super(ModeOpening1, self).__init__()

        self.time = 0
        self.step = 0
        self.background = pygame.Surface(constants.SCREEN_SIZE).convert(shared.display.screen)
        self.background.fill(constants.WHITE)
        shared.font_wrap.renderToCentered(
            self.background,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 5 // 8),
            self.__class__.logo_text,
            False,
            constants.BLACK
        )
        # replace this with new other
        logo = pygame.image.load(constants.JK_LOGO_BLACK).convert(shared.display.screen)
        self.background.blit(
            logo,
            (
                constants.SCREEN_SIZE[0] // 2 - logo.get_width() // 2,
                constants.SCREEN_SIZE[1] * 7 // 16 - logo.get_height() // 2,
            )
        )

    def _changeMode(self):
        self.next_mode = ModeOpening2()

    def _input(self, event):
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self._changeMode()

    def _update(self, dt):
        self.time += dt
        if self.time >= 1250 and self.step < 1:
            self.step += 1
            pass
        if self.time >= 1500 and self.step < 2:
            self.step += 1
            pass
        if self.time >= 1750 and self.step < 3:
            self.step += 1
            pass
        if self.time >= 4250:
            self._changeMode()

    def _drawScreen(self, screen):
        screen.blit(self.background, (0, 0))
