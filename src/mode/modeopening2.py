import pygame
import jovialengine

import constants
from sprite import Monster
from .modeopening3 import ModeOpening3
from .modeopening import ModeOpening


class ModeOpening2(ModeOpening):
    __slots__ = (
        '_time',
        '_fade',
        '_music_started',
        '_music_time',
        '_move_time',
    )

    def __init__(self):
        super().__init__()
        pygame.mixer.music.load(constants.TITLE_INTRO)
        self._music_started = False
        left_mon = Monster.at_level(3)
        right_mon = Monster.at_level(2)

        ground_level = constants.SCREEN_SIZE[1] - 32
        # starts at right
        left_mon.rect.bottomright = (constants.SCREEN_SIZE[0], ground_level)
        left_mon.reset_pos()
        left_mon.set_image(True)
        # starts at left
        right_mon.rect.bottomleft = (0, ground_level)
        right_mon.reset_pos()
        # move to the positions
        beat = 250
        pause = 50
        left_mon.add_pos_rel(Monster.LERP, beat * 6, (-constants.SCREEN_SIZE[0] // 2, 0))
        right_mon.add_pos_rel(Monster.LERP, beat * 6, (constants.SCREEN_SIZE[0] // 2, 0),
                              sound=jovialengine.load.sound(constants.SPROING), positional_sound=True)
        self._music_time = beat * 6
        # back and forth
        left_mon.add_wait(beat * 8 + pause * 2)
        jump = right_mon.rect.width // 8
        right_mon.add_pos_rel(Monster.LERP, beat, (jump, -jump))
        right_mon.add_pos_rel(Monster.LERP, beat, (jump, jump),
                              sound=jovialengine.load.sound(constants.SPROING), positional_sound=True)
        right_mon.add_pos_rel(Monster.LERP, beat, (-jump, -jump))
        right_mon.add_pos_rel(Monster.LERP, beat, (-jump, jump))
        right_mon.add_wait(pause, sound=jovialengine.load.sound(constants.SPROING), positional_sound=True)
        right_mon.add_pos_rel(Monster.LERP, beat, (jump, -jump))
        right_mon.add_pos_rel(Monster.LERP, beat, (jump, jump),
                              sound=jovialengine.load.sound(constants.SPROING), positional_sound=True)
        right_mon.add_pos_rel(Monster.LERP, beat, (-jump, -jump))
        right_mon.add_pos_rel(Monster.LERP, beat, (-jump, jump))
        right_mon.add_wait(pause)
        # small pause
        left_mon.add_wait(beat)
        right_mon.add_wait(beat)
        # slash!
        left_mon.add_pos_rel(Monster.LERP, 100, (-jump // 2, -jump // 3))
        left_mon.add_pos_rel(Monster.LERP, 200, (jump + jump // 2, jump // 3),
                             sound=jovialengine.load.sound(constants.THUNK), positional_sound=True)
        right_mon.add_wait(300)
        # jump back
        left_mon.add_wait(beat)
        right_mon.add_pos_rel(Monster.LERP, beat // 2, (jump * 2, -jump * 2))
        right_mon.add_pos_rel(Monster.LERP, beat // 2, (jump * 2, jump * 2))
        # pause
        left_mon.add_wait(150)
        left_mon.add_pos_rel(Monster.LERP, 100, (-jump, 0))
        right_mon.add_wait(beat * 3,
                           sound=jovialengine.load.sound(constants.SPROING), positional_sound=True)
        # back and forth again
        right_mon.add_pos_rel(Monster.LERP, beat, (-jump, -jump * 2))
        right_mon.add_pos_rel(Monster.LERP, beat, (-jump, jump * 2),
                              sound=jovialengine.load.sound(constants.SPROING), positional_sound=True)
        right_mon.add_pos_rel(Monster.LERP, beat, (jump, -jump * 2))
        right_mon.add_pos_rel(Monster.LERP, beat, (jump, jump * 2))
        # charge
        right_mon.add_wait(beat)
        right_mon.add_pos_rel(Monster.LERP, beat, (jump // 2, jump // 2))
        # fire
        right_mon.add_wait(beat * 2)
        right_mon.add_pos_rel(Monster.LERP, beat, (-jump * 6 - jump // 2, -jump * 2 - jump // 2),
                              sound=jovialengine.load.sound(constants.FSSSH))

        # higher layer = draw later = "in front"
        self.sprites_all.add(left_mon, layer=1)
        self.sprites_all.add(right_mon, layer=0)
        self._time = 0
        self._move_time = beat * 28 + pause * 2 + 300
        self._fade = pygame.Surface(constants.SCREEN_SIZE).convert()
        self._fade.fill(constants.WHITE)
        self._fade.set_alpha(0)

    def _switch_mode(self):
        self.next_mode = ModeOpening3()

    def _update_pre_sprites(self, dt):
        self._time += dt
        if self._time >= self._music_time and not self._music_started:
            pygame.mixer.music.play(1, fade_ms=2100)
            self._music_started = True
        if self._time >= self._move_time:
            self._fade.set_alpha(
                min((self._time - self._move_time) * 255 // 750, 255)
            )
        if self._time >= self._move_time + 1500:
            self._stop_mixer()
            self._switch_mode()

    def _draw_pre_sprites(self, screen):
        screen.fill(constants.WHITE)

    def _draw_post_camera(self, screen):
        screen.blit(self._fade, (0, 0))
