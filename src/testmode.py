import pygame

import constants
import shared
from gamemode import GameMode
from monster import Monster

class TestMode(GameMode):
    fill = (0, 200, 0)
    test_text = "01234567890123456789"

    __slots__ = (
        '_test_mon_pos',
    )

    def _createMonster(self):
        shared.state.protag_mon = Monster()
        self._test_mon_pos = [160,122]

    def __init__(self):
        super(TestMode, self).__init__()
        self._createMonster()

    def _input(self, event):
        if event.type == pygame.MOUSEMOTION:
            self._test_mon_pos = list(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._createMonster()
            elif event.key == pygame.K_l:
                shared.state.protag_mon.levelUp()

    def update(self):
        self._test_mon_pos[0] += self._keyStatus(pygame.K_RIGHT) - self._keyStatus(pygame.K_LEFT)
        self._test_mon_pos[1] += self._keyStatus(pygame.K_DOWN) - self._keyStatus(pygame.K_UP)

    def _drawScreen(self, screen):
        # clear of old draws
        screen.fill(self.__class__.fill)
        # make new draws
        shared.state.protag_mon.drawStanding(screen, self._test_mon_pos)
        shared.font_wrap.renderToInside(screen, (0,0), constants.SCREEN_SIZE[0]//2, self.__class__.test_text, False, constants.BLACK, constants.WHITE)
        shared.font_wrap.renderToInside(screen, (constants.SCREEN_SIZE[0]//2,0), constants.SCREEN_SIZE[0]//2, "Lorem", False, (255,0,0))
        # screen.blit(shared.font_wrap.renderInside(constants.SCREEN_SIZE[0]//2, self.__class__.test_text, False, constants.BLACK, constants.WHITE), (0,0))
        # screen.blit(shared.font_wrap.renderInside(constants.SCREEN_SIZE[0]//2, "Lorem", False, (255,0,0)), (constants.SCREEN_SIZE[0]//2,0))
