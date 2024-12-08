import jovialengine

import constants
from .modeopening1 import ModeOpening1
from .modeopening import ModeOpening
from sprite import Star


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
        jovialengine.get_default_font_wrap().render_to_centered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 5 // 8),
            self._LOGO_TEXT,
            constants.BLACK
        )
        logo = jovialengine.load.image(constants.JK_LOGO_BLACK)
        self._background.blit(
            logo,
            (
                constants.SCREEN_SIZE[0] // 2 - logo.get_width() // 2,
                constants.SCREEN_SIZE[1] * 7 // 16 - logo.get_height() // 2,
            )
        )
        print("MAKING STAR")
        star_sprite = Star((constants.SCREEN_SIZE[0] // 2 + constants.SCREEN_SIZE[0] // 20 * 7, 0 - 40 // 2))
        star_sprite.add_wait(750, sound=jovialengine.load.sound(constants.LONGSLIDE), positional_sound=True)
        star_sprite.add_pos_abs(
            jovialengine.AnimSprite.LERP,
            500,
            (
                constants.SCREEN_SIZE[0] // 2 - constants.SCREEN_SIZE[0] // 20 * 7,
                constants.SCREEN_SIZE[1] + star_sprite.rect.height // 2
            )
        )
        self.sprites_all.add(star_sprite)

    def _switch_mode(self):
        self.next_mode = ModeOpening1()

    def _update_pre_sprites(self, dt):
        self._time += dt
        if self._time >= 1250 and self._step < 1:
            self._step += 1
            jovialengine.get_default_font_wrap().render_to_centered(
                self._background,
                (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 5 // 8),
                self._LOGO_TEXT,
                constants.TEXT_COLOR
            )
        if self._time >= 1500 and self._step < 2:
            self._step += 1
            jovialengine.get_default_font_wrap().render_to_centered(
                self._background,
                (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 5 // 8),
                self._LOGO_TEXT,
                constants.DARK_TEXT_COLOR
            )
            logo = jovialengine.load.image(constants.JK_LOGO_LIGHT_GREY)
            self._background.blit(
                logo,
                (
                    constants.SCREEN_SIZE[0] // 2 - logo.get_width() // 2,
                    constants.SCREEN_SIZE[1] * 7 // 16 - logo.get_height() // 2,
                )
            )
        if self._time >= 1750 and self._step < 3:
            self._step += 1
            jovialengine.get_default_font_wrap().render_to_centered(
                self._background,
                (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 5 // 8),
                self._LOGO_TEXT,
                constants.BLACK
            )
            logo = jovialengine.load.image(constants.JK_LOGO_GREY)
            self._background.blit(
                logo,
                (
                    constants.SCREEN_SIZE[0] // 2 - logo.get_width() // 2,
                    constants.SCREEN_SIZE[1] * 7 // 16 - logo.get_height() // 2,
                )
            )
        if self._time >= 4000:
            self._stop_mixer()
            self._switch_mode()
