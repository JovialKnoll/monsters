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

    def __init__(self):
        super().__init__()
        if not constants.SCREEN_RECT.colliderect(shared.state.protag_mon.rect):
            shared.state.protag_mon.rect.midbottom = (160, 122)
        self.all_sprites.add(shared.state.protag_mon)
        self.dx = 0
        self.dy = 0

    def save(self):
        return {
            'dx': self.dx,
            'dy': self.dy,
        }

    @classmethod
    def load(cls, save_data):
        new_obj = cls()
        new_obj.dx = save_data['dx']
        new_obj.dy = save_data['dy']
        return new_obj

    def _input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                shared.state.protag_mon.kill()
                shared.state.protag_mon = Monster()
                shared.state.protag_mon.rect.midbottom = (160, 122)
                self.all_sprites.add(shared.state.protag_mon)
            elif event.key == pygame.K_l:
                shared.state.protag_mon.levelUp()

    def update(self, dt):
        pressed_keys = pygame.key.get_pressed()
        x_movement = pressed_keys[pygame.K_RIGHT] - pressed_keys[pygame.K_LEFT]
        y_movement = pressed_keys[pygame.K_DOWN] - pressed_keys[pygame.K_UP]

        self.dx, dx_int = utility.getIntMovement(
            self.dx,
            x_movement * .1,
            dt
        )
        self.dy, dy_int = utility.getIntMovement(
            self.dy,
            y_movement * .1,
            dt
        )

        if x_movement == 0:
            self.dx = 0
        if y_movement == 0:
            self.dy = 0

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
