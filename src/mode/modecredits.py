import pygame
import jovialengine

import constants
from .modeopening0 import ModeOpening0
from .modeopening import ModeOpening


class ModeCredits(ModeOpening):
    __slots__ = (
        '_credits_sprite',
        '_time',
        '_move_time',
        '_final_text',
    )

    def __init__(self):
        super().__init__()
        with open(constants.CREDITS_TEXT) as credits_file:
            credits_text = credits_file.read().replace(' ', '_')
        self._credits_sprite = jovialengine.AnimSprite()
        self._credits_sprite.image = jovialengine.shared.font_wrap.renderInside(
            constants.SCREEN_SIZE[0] * 3 // 4,
            credits_text,
            False,
            constants.WHITE,
            background=constants.BLACK
        )
        self._credits_sprite.rect = self._credits_sprite.image.get_rect()
        self._credits_sprite.rect.topleft = (
            constants.SCREEN_SIZE[0] // 4,
            constants.SCREEN_SIZE[1],
        )
        self._time = 0
        self._credits_sprite.addWait(1000)
        self._move_time = 1000
        credits_speed = constants.FONT_HEIGHT / 500
        credits_distance = constants.SCREEN_SIZE[1] + self._credits_sprite.rect.height
        credits_time = int(credits_distance / credits_speed)
        self._move_time += credits_time
        self._credits_sprite.addPosRel(
            jovialengine.AnimSprite.Lerp,
            credits_time,
            0,
            credits_distance * -1
        )
        self._credits_sprite.addWait(1000)
        self._move_time += 1000
        self._all_sprites.add(self._credits_sprite)
        self._final_text = pygame.Surface(constants.SCREEN_SIZE).convert()
        self._final_text.fill(constants.BLACK)
        jovialengine.shared.font_wrap.renderToCentered(
            self._final_text,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 2),
            "press any key to proceed",
            False,
            constants.WHITE
        )
        self._final_text.set_alpha(0)

    def _switchMode(self):
        self.next_mode = ModeOpening0()

    def _update(self, dt):
        self._time += dt
        if self._time >= self._move_time:
            self._final_text.set_alpha(
                min((self._time - self._move_time) * 255 // 1000, 255)
            )

    def _drawPreSprites(self, screen):
        screen.fill(constants.BLACK)
        screen.blit(self._final_text, (0, 0))
