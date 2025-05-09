import pygame
import jovialengine

import constants
from .modeopening0 import ModeOpening0
from .modeopening import ModeOpening


class ModeCredits(ModeOpening):
    __slots__ = (
        '_wait_song',
        '_playing_song',
        '_credits_sprite',
        '_time',
        '_move_time',
        '_final_text',
    )

    def __init__(self):
        super().__init__()
        pygame.mixer.music.load(constants.CREDITS_PLAY)
        pygame.mixer.music.set_volume(0.5)
        self._wait_song = 1000
        self._playing_song = False
        with open(constants.CREDITS_TEXT) as credits_file:
            credits_text = credits_file.read().replace(' ', '_')
        self._credits_sprite = jovialengine.AnimSprite()
        self._credits_sprite.image = jovialengine.get_default_font_wrap().render_inside(
            constants.SCREEN_SIZE[0] * 3 // 4,
            credits_text,
            constants.WHITE,
            constants.BLACK
        )
        self._credits_sprite.rect = self._credits_sprite.image.get_rect(topleft=
            (constants.SCREEN_SIZE[0] // 4, constants.SCREEN_SIZE[1]))
        self._time = 0
        self._credits_sprite.add_wait(1000)
        self._move_time = 1000
        credits_speed = constants.FONT_HEIGHT / 500
        credits_distance = constants.SCREEN_SIZE[1] + self._credits_sprite.rect.height
        credits_time = int(credits_distance / credits_speed)
        self._move_time += credits_time
        self._credits_sprite.add_pos_rel(
            jovialengine.AnimSprite.LERP,
            credits_time,
            (0, credits_distance * -1)
        )
        self._credits_sprite.add_wait(1000)
        self._move_time += 1000
        self.sprites_all.add(self._credits_sprite)
        self._final_text = pygame.Surface(constants.SCREEN_SIZE).convert()
        self._final_text.fill(constants.BLACK)
        jovialengine.get_default_font_wrap().render_to_centered(
            self._final_text,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 2),
            "press any key to proceed",
            constants.WHITE
        )
        self._final_text.set_alpha(0)

    def _switch_mode(self):
        jovialengine.set_state()
        next_mode_cls = jovialengine.get_restart_mode_cls()
        self.next_mode = next_mode_cls()

    def _update_pre_sprites(self, dt):
        if not self._playing_song:
            self._wait_song -= dt
            if self._wait_song <= 0:
                pygame.mixer.music.play(1, fade_ms=500)
                self._playing_song = True
        self._time += dt

    def _update_pre_draw(self):
        if self._time >= self._move_time:
            self._final_text.set_alpha(
                min((self._time - self._move_time) * 255 // 1000, 255)
            )

    def _draw_post_camera(self, screen):
        screen.blit(self._final_text)
