import pygame

import constants
import utility
import shared
from monster import Monster

from saveable import Saveable
from .mode import Mode


class ModeTest(Mode, Saveable):
    FILL = (31, 31, 31)
    TEST_TEXT = "01234567890123456789"

    def _createMonster(self):
        shared.state.protag_mon.kill()
        shared.state.protag_mon = Monster()
        shared.state.protag_mon.rect.midbottom = (160, 122)
        self.all_sprites.add(shared.state.protag_mon)

    def __init__(self):
        super().__init__()
        self._createMonster()
        self.dx = 0
        self.dy = 0

    def save(self):
        # todo: actually return object
        return 1

    @classmethod
    def load(cls, save_data):
        # todo: actually use save_data
        return cls()

    def _input(self, event):
        if event.type == pygame.MOUSEMOTION:
            shared.state.protag_mon.rect.midbottom = event.pos
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._createMonster()
            elif event.key == pygame.K_l:
                shared.state.protag_mon.levelUp()

    def update(self, dt):
        self.dx, dx_int = utility.getIntMovement(
            self.dx,
            (pygame.key.get_pressed()[pygame.K_RIGHT] - pygame.key.get_pressed()[pygame.K_LEFT]) * .1,
            dt
        )
        self.dy, dy_int = utility.getIntMovement(
            self.dy,
            (pygame.key.get_pressed()[pygame.K_DOWN] - pygame.key.get_pressed()[pygame.K_UP]) * .1,
            dt
        )
        shared.state.protag_mon.rect.move_ip(dx_int, dy_int)

    def _drawScreen(self, screen):
        # clear of old draws
        screen.fill(self.FILL)
        # make new draws
        shared.font_wrap.renderToInside(
            screen,
            (0, 0),
            constants.SCREEN_SIZE[0]//2,
            self.TEST_TEXT,
            False,
            constants.BLACK,
            constants.WHITE
        )
        shared.font_wrap.renderToInside(
            screen,
            (constants.SCREEN_SIZE[0] // 2, 0),
            constants.SCREEN_SIZE[0] // 2,
            "Lorem",
            False,
            (255, 0, 0)
        )
        # screen.blit(shared.font_wrap.renderInside(constants.SCREEN_SIZE[0]//2, self.TEST_TEXT, False, constants.BLACK, constants.WHITE), (0,0))
        # screen.blit(shared.font_wrap.renderInside(constants.SCREEN_SIZE[0]//2, "Lorem", False, (255,0,0)), (constants.SCREEN_SIZE[0]//2,0))
