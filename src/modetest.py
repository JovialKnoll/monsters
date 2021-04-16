import pygame

import constants
import utility
import shared
from mode import Mode
from monster import Monster

class ModeTest(Mode):
    fill = (31, 31, 31)
    test_text = "01234567890123456789"

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
            (self._keyStatus(pygame.K_RIGHT) - self._keyStatus(pygame.K_LEFT)) * .1,
            dt
        )
        self.dy, dy_int = utility.getIntMovement(
            self.dy,
            (self._keyStatus(pygame.K_DOWN) - self._keyStatus(pygame.K_UP)) * .1,
            dt
        )
        shared.state.protag_mon.rect.move_ip(dx_int, dy_int)

    def _drawScreen(self, screen):
        # clear of old draws
        screen.fill(self.__class__.fill)
        # make new draws
        shared.font_wrap.renderToInside(
            screen,
            (0, 0),
            constants.SCREEN_SIZE[0]//2,
            self.__class__.test_text,
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
        # screen.blit(shared.font_wrap.renderInside(constants.SCREEN_SIZE[0]//2, self.__class__.test_text, False, constants.BLACK, constants.WHITE), (0,0))
        # screen.blit(shared.font_wrap.renderInside(constants.SCREEN_SIZE[0]//2, "Lorem", False, (255,0,0)), (constants.SCREEN_SIZE[0]//2,0))
