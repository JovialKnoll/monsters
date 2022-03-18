import math

import pygame
import jovialengine

import constants
from .modeopening2 import ModeOpening2
from .modeopening import ModeOpening


class ModeOpening1(ModeOpening):
    _STAR_WAVES = 3
    _STAR_WAIT = 1000
    _STAR_TRAVEL = 350

    __slots__ = (
        '_time',
        '_logo',
    )

    def __init__(self):
        super().__init__()

        self._time = 0
        self._background.fill(constants.WHITE)
        jovialengine.shared.font_wrap.renderToCentered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 5 // 8 + 8),
            "tinsil",
            False,
            constants.BLACK
        )
        bip = pygame.mixer.Sound(constants.BIP)
        self._logo = pygame.image.load(constants.TIN_LOGO).convert()
        self._logo.set_colorkey(constants.COLORKEY)
        star_image = pygame.image.load(constants.STAR).convert()
        star_image.set_colorkey(constants.COLORKEY)
        star_image = pygame.transform.scale(
            star_image,
            (
                star_image.get_width() // 2,
                star_image.get_height() // 2,
            )
        )
        star_number = 7
        for i in range(self._STAR_WAVES):
            for j in range(star_number):
                radius = constants.SCREEN_SIZE[0] * 5 // 8
                angle = j * 2 / star_number * math.pi
                x = constants.SCREEN_SIZE[0] // 2 + radius * math.sin(angle)
                y = constants.SCREEN_SIZE[1] // 2 - radius * math.cos(angle)
                self._makeStar(
                    star_image,
                    self._STAR_WAIT + i * self._STAR_TRAVEL,
                    (x, y),
                    bip if j == 0 else None
                )

    def _makeStar(self, image: pygame.Surface, wait: int, dest: tuple[int, int], sound):
        star_sprite = jovialengine.AnimSprite()
        star_sprite.image = image
        star_sprite.rect = star_sprite.image.get_rect()
        star_sprite.rect.center = (
            constants.SCREEN_SIZE[0] // 2,
            constants.SCREEN_SIZE[1] // 2,
        )
        star_sprite.addWait(wait, sound=sound)
        star_sprite.addPosAbs(
            jovialengine.AnimSprite.Lerp,
            self._STAR_TRAVEL,
            dest
        )
        self._all_sprites.add(star_sprite)

    def _switchMode(self):
        self.next_mode = ModeOpening2()

    def _update(self, dt):
        self._time += dt
        if self._time >= self._STAR_WAIT * 2 + self._STAR_TRAVEL * self._STAR_WAVES:
            self._stopMixer()
            self._switchMode()

    def _drawPostSprites(self, screen):
        screen.blit(
            self._logo,
            (
                constants.SCREEN_SIZE[0] // 2 - self._logo.get_width() // 2,
                constants.SCREEN_SIZE[1] * 7 // 16 - self._logo.get_height() // 2,
            )
        )
