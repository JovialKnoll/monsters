import random
import itertools
import math
from collections import deque

import pygame
import jovialengine

import constants
from monster import Monster
from .modebuttons import ModeButtons


class ModeFight(ModeButtons):
    buttons = (
        pygame.Rect(24, 24, 88, 36),
        pygame.Rect(24, 76, 88, 36),
        pygame.Rect(24, 128, 88, 36),
    )
    _PLAYER_POS = (170, 128)
    _ENEMY_POS = (262, 128)
    _ANIM_WAIT = 250
    _HEALTH_BAR_LENGTH = 60
    _HEALTH_BAR_HEIGHT = 10
    _BOX_CHOICES = [
        constants.FIGHT_ATTACK,
        constants.FIGHT_DEFEND,
        constants.FIGHT_DODGE,
    ]
    _RESULT_SAVING = {
        'draw': 0,
        'win': 1,
        'lose': -1,
    }
    _PLAYER_BAR_X = 137
    _ENEMY_BAR_X = 233
    _PLAYER_BAR_Y = _ENEMY_BAR_Y = 29

    __slots__ = (
        '_health_bar',
        '_player_mon',
        '_enemy_mon',
        '_enemy_choices',
        '_user_interface',
        '_player_action',
        '_enemy_action',
        '_action_display',
        '_action_display_latest',
        '_action_display_latest2',
        '_action_set',
        '_result_displayed',
        '_result',
        '_get_next_mode',
        '_camera_shake',
    )

    def __init__(self, player_mon: Monster, enemy_mon: Monster, get_next_mode: callable):
        """The functions passed in should return the next mode."""
        super().__init__()
        self._background.fill(constants.WHITE)
        self._health_bar = jovialengine.load.image(constants.HEALTHBAR_FILE, constants.COLORKEY)

        self._player_mon = player_mon
        self._enemy_mon = enemy_mon
        self._enemy_choices = self._BOX_CHOICES \
            + list(itertools.repeat(self._enemy_mon.personality.preferred_action, 3))

        self._user_interface = jovialengine.load.image(constants.LAYOUT_2_FILE, constants.COLORKEY).copy()
        for index, choice in enumerate(self._BOX_CHOICES):
            jovialengine.get_default_font_wrap().render_to_inside(
                self._user_interface,
                self._text_start(index),
                self._text_width(index),
                choice,
                constants.TEXT_COLOR
            )

        pygame.mixer.music.load(constants.FIGHT_LOOP)
        pygame.mixer.music.play(-1)

        self._player_mon.fight_start()
        self._player_mon.set_image(True)

        self._enemy_mon.fight_start()
        self._enemy_mon.set_image(False)

        self._player_mon.rect.midbottom = self._PLAYER_POS
        self._enemy_mon.rect.midbottom = self._ENEMY_POS
        self.sprite_groups["all"].add(self._player_mon, self._enemy_mon)

        self._player_action: bool | str = False
        self._enemy_action: bool | str = False

        self._action_display = deque((), 4)
        self._action_display_latest = None
        self._action_display_latest2 = None
        self._action_set = False

        self._result_displayed = 0
        self._result = False
        self._get_next_mode = get_next_mode

        self._camera_shake = None

        self._draw_hp()

    def _draw_hp(self):
        player_health_text = f"{self._player_mon.stats['hpc']}/{self._player_mon.stats['hpm']}"
        if self._player_mon.stats['hpc'] < 10:
            player_health_text = "_" + player_health_text
        enemy_health_text = f"{self._enemy_mon.stats['hpc']}/{self._enemy_mon.stats['hpm']}"
        if self._enemy_mon.stats['hpc'] < 10:
            enemy_health_text = "_" + enemy_health_text
        text_width = constants.FONT_SIZE * 5
        player_health_dest = (
            self._PLAYER_BAR_X + self._HEALTH_BAR_LENGTH + 2 - text_width,
            self._PLAYER_BAR_Y - constants.FONT_HEIGHT
        )
        enemy_health_dest = (
            self._ENEMY_BAR_X + self._HEALTH_BAR_LENGTH + 2 - text_width,
            self._ENEMY_BAR_Y - constants.FONT_HEIGHT
        )
        jovialengine.get_default_font_wrap().render_to_inside(
            self._user_interface,
            player_health_dest,
            text_width,
            player_health_text,
            constants.TEXT_COLOR,
            constants.WHITE
        )
        jovialengine.get_default_font_wrap().render_to_inside(
            self._user_interface,
            enemy_health_dest,
            text_width,
            enemy_health_text,
            constants.TEXT_COLOR,
            constants.WHITE
        )

    def _shake_camera(self):
        if self._camera_shake is None:
            if bool(random.getrandbits(1)):
                self._camera.x -= 1
            else:
                self._camera.x += 1
            if bool(random.getrandbits(1)):
                self._camera.y -= 1
            else:
                self._camera.y += 1
            self._camera_shake = 50

    def _reset_camera(self):
        self._camera_shake = None
        self._camera.x = 0
        self._camera.y = 0

    def _button_press(self):
        self._player_action = self._BOX_CHOICES[self._selected_button]
        self._enemy_action = random.choice(self._enemy_choices)

        if self._player_action == constants.FIGHT_ATTACK:
            self._set_action_display("I'm gonna hit 'em!")
            self._player_mon.add_wait(self._ANIM_WAIT)
            self._player_mon.add_pos_rel(jovialengine.AnimSprite.LERP, 200, 12, 0,
                                         sound=jovialengine.load.sound(constants.THUNK), positional_sound=True,
                                         callback=self._shake_camera)
            self._player_mon.add_pos_rel(jovialengine.AnimSprite.LERP, 200, -12, 0)
        elif self._player_action == constants.FIGHT_DEFEND:
            self._set_action_display("I'm gonna block 'em!")
            self._player_mon.add_wait(self._ANIM_WAIT)
            self._player_mon.add_pos_rel(jovialengine.AnimSprite.LERP, 133, -8, 0,
                                         sound=jovialengine.load.sound(constants.BWOP), positional_sound=True,
                                         callback=self._shake_camera)
            self._player_mon.add_pos_rel(jovialengine.AnimSprite.LERP, 200, 12, 0)
            self._player_mon.add_pos_rel(jovialengine.AnimSprite.LERP, 67, -4, 0)
        elif self._player_action == constants.FIGHT_DODGE:
            self._set_action_display("I'm gonna dodge!")
            self._player_mon.add_wait(self._ANIM_WAIT)
            self._player_mon.add_wait(0, sound=jovialengine.load.sound(constants.ROOEEE), positional_sound=True)
            self._player_mon.add_pos_rel(jovialengine.AnimSprite.LERP, 333, -20, 0)
            self._player_mon.add_pos_rel(jovialengine.AnimSprite.LERP, 67, 20, 0)

        if self._enemy_action == constants.FIGHT_ATTACK:
            self._enemy_mon.add_wait(self._ANIM_WAIT)
            self._enemy_mon.add_pos_rel(jovialengine.AnimSprite.LERP, 200, -12, 0,
                                        sound=jovialengine.load.sound(constants.THUNK), positional_sound=True,
                                        callback=self._shake_camera)
            self._enemy_mon.add_pos_rel(jovialengine.AnimSprite.LERP, 200, 12, 0)
        elif self._enemy_action == constants.FIGHT_DEFEND:
            self._enemy_mon.add_wait(self._ANIM_WAIT)
            self._enemy_mon.add_pos_rel(jovialengine.AnimSprite.LERP, 133, 8, 0,
                                        sound=jovialengine.load.sound(constants.BWOP), positional_sound=True,
                                        callback=self._shake_camera)
            self._enemy_mon.add_pos_rel(jovialengine.AnimSprite.LERP, 200, -12, 0)
            self._enemy_mon.add_pos_rel(jovialengine.AnimSprite.LERP, 67, 4, 0)
        elif self._enemy_action == constants.FIGHT_DODGE:
            self._enemy_mon.add_wait(self._ANIM_WAIT)
            self._enemy_mon.add_wait(0, sound=jovialengine.load.sound(constants.ROOEEE), positional_sound=True)
            self._enemy_mon.add_pos_rel(jovialengine.AnimSprite.LERP, 333, 20, 0)
            self._enemy_mon.add_pos_rel(jovialengine.AnimSprite.LERP, 67, -20, 0)

    def _end_fight(self):
        self._stop_mixer()
        jovialengine.get_state().fight_results.append(self._RESULT_SAVING[self._result])
        self.next_mode = self._get_next_mode()

    def _take_event(self, event):
        # click forward to next mode
        if self._result:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self._end_fight()
                return
        # in the middle of action display
        if self._player_action:
            return
        super()._take_event(event)

    def _take_frame(self, input_frame):
        # click forward to next mode
        if self._result:
            if input_frame.was_input_pressed(constants.EVENT_CONFIRM):
                self._end_fight()
                return
        # in the middle of action display
        if self._player_action:
            return
        super()._take_frame(input_frame)
        if input_frame.was_input_pressed(constants.EVENT_UP):
            self._key_select(-1)
        if input_frame.was_input_pressed(constants.EVENT_DOWN):
            self._key_select(1)

    def _set_action_display(self, text: str):
        self._action_display.appendleft(
            jovialengine.get_default_font_wrap().render_inside(
                200,
                text,
                constants.TEXT_COLOR,
                constants.WHITE
            )
        )
        self._action_display_latest = jovialengine.get_default_font_wrap().render_inside(
            200,
            text,
            constants.BLACK,
            constants.WHITE
        )
        self._action_set = not self._action_set

    def _player_action_done(self):
        player_hit_block = self._player_mon.fight_hit(self._player_action, True)
        enemy_hit_block = self._enemy_mon.fight_hit(self._enemy_action)

        raw_player_damage = enemy_hit_block[0] - player_hit_block[1]
        final_player_damage = jovialengine.utility.reduce_number(
            max(
                0,
                raw_player_damage
            ),
            2
        )
        raw_enemy_damage = player_hit_block[0] - enemy_hit_block[1]
        final_enemy_damage = jovialengine.utility.reduce_number(
            max(
                0,
                raw_enemy_damage
            ),
            2
        )
        if final_player_damage == 0 and final_enemy_damage == 0:
            if raw_player_damage > raw_enemy_damage:
                final_player_damage = 1
            elif raw_enemy_damage > raw_player_damage:
                final_enemy_damage = 1
            else:
                final_player_damage = final_enemy_damage = 1
        # display results below
        self._set_action_display("Hit for " + str(final_enemy_damage) + "! Took " + str(final_player_damage) + "!")
        self._player_mon.stats['hpc'] -= final_player_damage
        self._player_mon.stats['hpc'] = max(self._player_mon.stats['hpc'], 0)
        self._enemy_mon.stats['hpc'] -= final_enemy_damage
        self._enemy_mon.stats['hpc'] = max(self._enemy_mon.stats['hpc'], 0)
        self._draw_hp()

        if self._player_mon.stats['hpc'] < 1 and self._enemy_mon.stats['hpc'] < 1:
            self._setup_end('draw')
        elif self._enemy_mon.stats['hpc'] < 1:
            self._setup_end('win')
        elif self._player_mon.stats['hpc'] < 1:
            self._setup_end('lose')
        else:
            self._player_action = False
        self._enemy_action = False

    def _setup_end(self, ending: str):
        self._player_action = ending
        self._player_mon.add_wait(750)
        self._player_mon.add_wait(750)
        pygame.mixer.music.fadeout(1000)

    def _update_pre_sprites(self, dt):
        if self._camera_shake is not None:
            self._camera_shake -= dt
            if self._camera_shake <= 0:
                self._reset_camera()
        if self._player_action in self._BOX_CHOICES and not self._player_mon.still_animating():
            self._player_action_done()
        elif self._player_action == 'draw':
            self._end_stuff("They're both out cold.")
        elif self._player_action == 'win':
            self._end_stuff("I won!!!")
        elif self._player_action == 'lose':
            self._end_stuff(self._player_mon.name + "'s out cold.")

    def _end_stuff(self, result_display: str):
        if len(self._player_mon.anims) < 2 and self._result_displayed < 1:
            self._set_action_display(result_display)
            self._result_displayed = 1
        elif not self._player_mon.still_animating() and self._result_displayed < 2:
            self._set_action_display("Click or press enter to")
            self._action_display_latest2 = jovialengine.get_default_font_wrap().render_inside(
                200,
                "Click or press enter to",
                constants.BLACK,
                constants.WHITE
            )
            self._set_action_display("continue.")
            self._result_displayed = 2
            self._result = self._player_action

    def _update_pre_draw(self, screen):
        screen.fill(constants.WHITE)

    def _draw_pre_sprites(self, screen):
        screen.blit(self._user_interface, (0, 0))
        if not self._action_set and self._player_action not in self._RESULT_SAVING:
            self._draw_selected(screen)

        player_bar_length = math.ceil(
            self._HEALTH_BAR_LENGTH
            * self._player_mon.stats['hpc'] / self._player_mon.stats['hpm']
        )
        screen.fill(
            self._player_mon.get_bar_color(),
            (
                self._PLAYER_BAR_X + 1,
                self._PLAYER_BAR_Y + 1,
                player_bar_length,
                self._HEALTH_BAR_HEIGHT - 2
            )
        )
        screen.fill(
            self._player_mon.get_bar_color2(),
            (
                self._PLAYER_BAR_X + 1,
                self._PLAYER_BAR_Y + self._HEALTH_BAR_HEIGHT - 1,
                player_bar_length,
                2
            )
        )
        screen.blit(self._health_bar, (self._PLAYER_BAR_X, self._PLAYER_BAR_Y))

        enemy_bar_length = math.ceil(
            self._HEALTH_BAR_LENGTH
            * self._enemy_mon.stats['hpc'] / self._enemy_mon.stats['hpm']
        )
        screen.fill(
            self._enemy_mon.get_bar_color(),
            (
                self._ENEMY_BAR_X + self._HEALTH_BAR_LENGTH + 1 - enemy_bar_length,
                self._ENEMY_BAR_Y + 1,
                enemy_bar_length,
                self._HEALTH_BAR_HEIGHT - 2
            )
        )
        screen.fill(
            self._enemy_mon.get_bar_color2(),
            (
                self._ENEMY_BAR_X + self._HEALTH_BAR_LENGTH + 1 - enemy_bar_length,
                self._ENEMY_BAR_Y + self._HEALTH_BAR_HEIGHT - 1,
                enemy_bar_length,
                2
            )
        )
        screen.blit(self._health_bar, (self._ENEMY_BAR_X, self._ENEMY_BAR_Y))
        for index, line in enumerate(self._action_display):
            screen.blit(line, (120, 166 - constants.FONT_HEIGHT * index))
        if self._action_display_latest:
            screen.blit(self._action_display_latest, (120, 166))
        if self._action_display_latest2:
            screen.blit(self._action_display_latest2, (120, 166 - constants.FONT_HEIGHT))
