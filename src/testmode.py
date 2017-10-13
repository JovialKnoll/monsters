import pygame

from gamemode import *
from monster import *
from constants import *

class TestMode(GameMode):
    def _createMonster(self):
        self.shared.protag_mon = Monster()
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
                self.shared.protag_mon.levelUp()

    def update(self):
        self.test_mon_pos[0] += self._keyStatus(pygame.K_RIGHT) - self._keyStatus(pygame.K_LEFT)
        self.test_mon_pos[1] += self._keyStatus(pygame.K_DOWN) - self._keyStatus(pygame.K_UP)

    def draw(self, screen):
        # clear of old draws
        screen.fill(self.fill)
        # make new draws
        self.shared.protag_mon.drawStanding(screen, self.test_mon_pos)
        self.shared.font_wrap.renderToInside(screen, (0,0), SCREEN_SIZE[0]//2, self.test_text, False, BLACK, WHITE)
        self.shared.font_wrap.renderToInside(screen, (SCREEN_SIZE[0]//2,0), SCREEN_SIZE[0]//2, "Lorem", False, (255,0,0))
        # screen.blit(self.shared.font_wrap.renderInside(SCREEN_SIZE[0]//2, self.test_text, False, BLACK, WHITE), (0,0))
        # screen.blit(self.shared.font_wrap.renderInside(SCREEN_SIZE[0]//2, "Lorem", False, (255,0,0)), (SCREEN_SIZE[0]//2,0))
