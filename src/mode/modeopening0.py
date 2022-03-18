import pygame
import jovialengine

import constants
from .modeopening1 import ModeOpening1
from .modeopening import ModeOpening


class ModeOpening0(ModeOpening):
    _LOGO_TEXT = "JovialKnoll"

    __slots__ = (
        '_time',
        '_step',
    )

    def __init__(self):
        super().__init__()
        self._time = 0
        self._step = 0
        self._background.fill(constants.WHITE)
        jovialengine.shared.font_wrap.renderToCentered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 5 // 8),
            self._LOGO_TEXT,
            False,
            constants.BLACK
        )
        logo = pygame.image.load(constants.JK_LOGO_BLACK).convert()
        self._background.blit(
            logo,
            (
                constants.SCREEN_SIZE[0] // 2 - logo.get_width() // 2,
                constants.SCREEN_SIZE[1] * 7 // 16 - logo.get_height() // 2,
            )
        )
        star_sprite = jovialengine.AnimSprite()
        star_sprite.image = pygame.image.load(constants.STAR).convert()
        star_sprite.image.set_colorkey(constants.COLORKEY)
        star_sprite.rect = star_sprite.image.get_rect()
        star_sprite.rect.center = (
            constants.SCREEN_SIZE[0] // 2 + constants.SCREEN_SIZE[1] // 2 + star_sprite.rect.width // 2,
            star_sprite.rect.height // 2 * -1,
        )
        star_sprite.addWait(750, sound=pygame.mixer.Sound(constants.LONGSLIDE), positional_sound=True)
        star_sprite.addPosAbs(
            jovialengine.AnimSprite.Lerp,
            500,
            constants.SCREEN_SIZE[0] // 2 - constants.SCREEN_SIZE[1] // 2 - star_sprite.rect.width // 2,
            constants.SCREEN_SIZE[1] + star_sprite.rect.height // 2
        )
        self._all_sprites.add(star_sprite)

    def _switchMode(self):
        self.next_mode = ModeOpening1()

    def _update(self, dt):
        self._time += dt
        if self._time >= 1250 and self._step < 1:
            self._step += 1
            jovialengine.shared.font_wrap.renderToCentered(
                self._background,
                (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 5 // 8),
                self._LOGO_TEXT,
                False,
                constants.TEXT_COLOR
            )
        if self._time >= 1500 and self._step < 2:
            self._step += 1
            jovialengine.shared.font_wrap.renderToCentered(
                self._background,
                (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 5 // 8),
                self._LOGO_TEXT,
                False,
                constants.DARK_TEXT_COLOR
            )
            logo = pygame.image.load(constants.JK_LOGO_LIGHT_GREY).convert()
            self._background.blit(
                logo,
                (
                    constants.SCREEN_SIZE[0] // 2 - logo.get_width() // 2,
                    constants.SCREEN_SIZE[1] * 7 // 16 - logo.get_height() // 2,
                )
            )
        if self._time >= 1750 and self._step < 3:
            self._step += 1
            jovialengine.shared.font_wrap.renderToCentered(
                self._background,
                (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 5 // 8),
                self._LOGO_TEXT,
                False,
                constants.BLACK
            )
            logo = pygame.image.load(constants.JK_LOGO_GREY).convert()
            self._background.blit(
                logo,
                (
                    constants.SCREEN_SIZE[0] // 2 - logo.get_width() // 2,
                    constants.SCREEN_SIZE[1] * 7 // 16 - logo.get_height() // 2,
                )
            )
        if self._time >= 4000:
            self._stopMixer()
            self._switchMode()
