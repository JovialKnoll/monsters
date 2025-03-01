import math

import pygame
import jovialengine

import constants
from .modeopening2 import ModeOpening2
from .modeopening import ModeOpening
from sprite import TinLogo


class ModeOpening1(ModeOpening):
    _STAR_WAVES = 3
    _STAR_COUNT = 7
    _STAR_WAIT = 1000
    _STAR_TRAVEL = 350

    __slots__ = (
        '_time',
    )

    def __init__(self):
        super().__init__()
        self._time = 0
        self._background.fill(constants.WHITE)
        jovialengine.get_default_font_wrap().render_to_centered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 5 // 8 + 8),
            "tinsil",
            constants.BLACK
        )
        star_image = jovialengine.load.image(constants.STAR, constants.COLORKEY)
        star_image = pygame.transform.scale(
            star_image,
            (
                star_image.get_width() // 2,
                star_image.get_height() // 2,
            )
        )
        for i in range(self._STAR_WAVES):
            for j in range(self._STAR_COUNT):
                radius = constants.SCREEN_SIZE[0] * 5 // 8
                angle = j * 2 / self._STAR_COUNT * math.pi
                x = constants.SCREEN_SIZE[0] // 2 + radius * math.sin(angle)
                y = constants.SCREEN_SIZE[1] // 2 - radius * math.cos(angle)
                self._make_star(
                    star_image,
                    self._STAR_WAIT + i * self._STAR_TRAVEL,
                    (x, y),
                    jovialengine.load.sound(constants.BIP) if j == 0 else None
                )
        logo = TinLogo(center=(constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 7 // 16))
        self.sprites_all.add(logo, layer=1)

    def _make_star(self, image: pygame.Surface, wait: int, dest: tuple[int, int], sound):
        star_sprite = jovialengine.AnimSprite()
        star_sprite.image = image
        star_sprite.rect = star_sprite.image.get_rect(center=
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 2))
        star_sprite.add_wait(wait, sound=sound)
        star_sprite.add_pos_abs(
            jovialengine.AnimSprite.LERP,
            self._STAR_TRAVEL,
            dest
        )
        self.sprites_all.add(star_sprite)

    def _switch_mode(self):
        self.next_mode = ModeOpening2()

    def _update_pre_sprites(self, dt):
        self._time += dt
        if self._time >= self._STAR_WAIT * 2 + self._STAR_TRAVEL * self._STAR_WAVES:
            self._stop_mixer()
            self._switch_mode()
