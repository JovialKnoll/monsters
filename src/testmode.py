import pygame
import constants
import sharedstate

from gamemode import *
from monster import *

class TestMode(GameMode):
    def _createMonster(self):
        sharedstate.state.protag_mon = Monster()
        self.test_mon_pos = [160,122]

    def __init__(self):
        super(TestMode, self).__init__()
        self.fill = (0, 200, 0)
        self._createMonster()
        self.test_text = "01234567890123456789"

    def _input(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.test_mon_pos = list(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._createMonster()
            elif event.key == pygame.K_l:
                sharedstate.state.protag_mon.levelUp()

    def update(self):
        self.test_mon_pos[0] += self._keyStatus(pygame.K_RIGHT) - self._keyStatus(pygame.K_LEFT)
        self.test_mon_pos[1] += self._keyStatus(pygame.K_DOWN) - self._keyStatus(pygame.K_UP)

    def _drawScreen(self, screen):
        # clear of old draws
        screen.fill(self.fill)
        # make new draws
        sharedstate.state.protag_mon.drawStanding(screen, self.test_mon_pos)
        sharedstate.state.font_wrap.renderToInside(screen, (0,0), constants.SCREEN_SIZE[0]//2, self.test_text, False, constants.BLACK, constants.WHITE)
        sharedstate.state.font_wrap.renderToInside(screen, (constants.SCREEN_SIZE[0]//2,0), constants.SCREEN_SIZE[0]//2, "Lorem", False, (255,0,0))
        # screen.blit(sharedstate.state.font_wrap.renderInside(constants.SCREEN_SIZE[0]//2, self.test_text, False, constants.BLACK, constants.WHITE), (0,0))
        # screen.blit(sharedstate.state.font_wrap.renderInside(constants.SCREEN_SIZE[0]//2, "Lorem", False, (255,0,0)), (constants.SCREEN_SIZE[0]//2,0))
