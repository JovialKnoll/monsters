import abc
import os
from collections import deque

import pygame
import jovialengine

import constants
from .modeopening import ModeOpening


class ModeLevelUp(ModeOpening, abc.ABC):
    __slots__ = (
        '_done',
        '_time',
        '_first_sprite',
        '_sprite_switches',
    )

    def _draw_font_effect(self, text: str, pos: tuple[int, int]):
        jovialengine.get_default_font_wrap().render_to_centered(
            self._background,
            (pos[0] + 1, pos[1] + 1),
            text,
            constants.TEXT_COLOR
        )
        jovialengine.get_default_font_wrap().render_to_centered(
            self._background,
            (pos[0], pos[1]),
            text,
            constants.DARK_TEXT_COLOR
        )

    def __init__(self):
        super().__init__()
        self._done = False
        self._time = 0
        self._background.fill(constants.WHITE)
        self._draw_font_effect("LEVEL UP", (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 4))
        jovialengine.get_state().protag_mon.set_image()
        # set up first sprite
        self._first_sprite = pygame.sprite.Sprite()
        self._first_sprite.image = jovialengine.get_state().protag_mon.image
        self._first_sprite.rect = jovialengine.get_state().protag_mon.rect
        self._first_sprite.rect.center = (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 2 // 3)
        # level up and set up second sprite
        jovialengine.get_state().protag_mon.level_up()
        jovialengine.get_state().protag_mon.set_image()
        jovialengine.get_state().protag_mon.rect.midbottom = self._first_sprite.rect.midbottom
        self.sprites_all.add(self._first_sprite)
        self._sprite_switches = deque((
            4000,
            4100,
            6000,
            6100,
            8000,
            8100,
            10000,
            10100,
            11000,
            11100,
            12000,
            12100,
            13000,
            13100,
            14000,
            14500,
            15000,
            15750,
            16000,
        ))
        try:
            os.mkdir(constants.IMAGE_DIRECTORY)
        except FileExistsError:
            pass
        file_name = \
            f"{jovialengine.get_state().protag_mon.name}_{jovialengine.get_state().protag_mon.uuid}.png"
        file_path = os.path.join(constants.IMAGE_DIRECTORY, file_name)
        pygame.image.save(jovialengine.get_state().protag_mon.get_card(), file_path)

    def _take_event(self, event):
        if self._time >= 16000:
            super()._take_event(event)

    def _take_frame(self, input_frame):
        if self._time >= 16000:
            super()._take_frame(input_frame)

    def _update_pre_sprites(self, dt):
        self._time += dt
        while self._sprite_switches and self._time >= self._sprite_switches[0]:
            self._switch_visible_sprite()
            self._sprite_switches.popleft()
        if not self._sprite_switches and not self._done:
            self._done = True
            self._draw_font_effect(
                "PRESS ANY KEY TO PROCEED",
                (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 4 + 2 * constants.FONT_HEIGHT)
            )

    def _switch_visible_sprite(self):
        jovialengine.load.sound(constants.BIP).play()
        if self._first_sprite.alive():
            self.sprites_all.remove(self._first_sprite)
            self.sprites_all.add(jovialengine.get_state().protag_mon)
        else:
            self.sprites_all.add(self._first_sprite)
            self.sprites_all.remove(jovialengine.get_state().protag_mon)
