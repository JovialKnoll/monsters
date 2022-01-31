import pygame

import constants
import shared
from animsprite import AnimSprite
from .modeopening0 import ModeOpening0
from .modeopening import ModeOpening


class ModeCredits(ModeOpening):
    __slots__ = (
        '_background',
        '_credits_sprite',
    )

    def __init__(self):
        super().__init__()
        self._background = pygame.Surface(constants.SCREEN_SIZE).convert(shared.display.screen)
        self._background.fill(constants.BLACK)
        with open(constants.CREDITS_TEXT) as credits_file:
            credits_text = credits_file.read().replace(' ', '_')
        self._credits_sprite = AnimSprite()
        self._credits_sprite.image = shared.font_wrap.renderInside(
            constants.SCREEN_SIZE[0] // 2,
            credits_text,
            False,
            constants.WHITE,
            background=constants.BLACK
        )
        self._credits_sprite.rect = self._credits_sprite.image.get_rect()
        self._credits_sprite.rect.midtop = (
            constants.SCREEN_SIZE[0] // 2,
            constants.SCREEN_SIZE[1],
        )
        self._credits_sprite.addWait(1000)
        credits_speed = constants.FONT_HEIGHT / 750
        credits_distance = constants.SCREEN_SIZE[1] + self._credits_sprite.rect.height
        credits_time = int(credits_distance / credits_speed)
        self._credits_sprite.addPosRel(
            AnimSprite.Lerp,
            credits_time,
            0,
            credits_distance * -1
        )
        self._credits_sprite.addWait(1000)
        self.all_sprites.add(self._credits_sprite)

    def _switchMode(self):
        self.next_mode = ModeOpening0()

    def _update(self, dt):
        if not self._credits_sprite.stillAnimating():
            shared.font_wrap.renderToCentered(
                self._background,
                (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 2 + 4),
                "press any key to proceed",
                False,
                constants.WHITE
            )

    def _drawScreen(self, screen):
        screen.blit(self._background, (0, 0))
