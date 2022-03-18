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
    _back_keys = {
        pygame.K_UP,
        pygame.K_LEFT,
        pygame.K_w,
        pygame.K_a,
    }
    _forward_keys = {
        pygame.K_DOWN,
        pygame.K_RIGHT,
        pygame.K_s,
        pygame.K_d,
    }
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
        '_thunk',
        '_rooeee',
        '_bwop',
        '_player_action',
        '_enemy_action',
        '_action_display',
        '_action_display_latest',
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
        self._health_bar = pygame.image.load(constants.HEALTHBAR_FILE).convert()
        self._health_bar.set_colorkey(constants.COLORKEY)

        self._player_mon = player_mon
        self._enemy_mon = enemy_mon
        self._enemy_choices = self._BOX_CHOICES \
            + list(itertools.repeat(self._enemy_mon.personality.preferred_action, 3))

        self._user_interface = pygame.image.load(constants.LAYOUT_2_FILE)
        for index, choice in enumerate(self._BOX_CHOICES):
            jovialengine.shared.font_wrap.renderToInside(
                self._user_interface,
                self._textStart(index),
                self._textWidth(index),
                choice,
                False,
                constants.TEXT_COLOR
            )
        self._user_interface = self._user_interface.convert()
        self._user_interface.set_colorkey(constants.COLORKEY)

        pygame.mixer.music.load(constants.FIGHT_LOOP)
        pygame.mixer.music.play(-1)

        self._thunk = pygame.mixer.Sound(constants.THUNK)
        self._rooeee = pygame.mixer.Sound(constants.ROOEEE)
        self._bwop = pygame.mixer.Sound(constants.BWOP)

        self._player_mon.fightStart()
        self._player_mon.setImage(True)

        self._enemy_mon.fightStart()
        self._enemy_mon.setImage(False)

        self._player_mon.rect.midbottom = self._PLAYER_POS
        self._enemy_mon.rect.midbottom = self._ENEMY_POS
        self._all_sprites.add(self._player_mon, self._enemy_mon)

        self._player_action = False
        self._enemy_action = False

        self._action_display = deque((), 4)
        self._action_display_latest = None
        self._action_set = False

        self._result_displayed = 0
        self._result = False
        self._get_next_mode = get_next_mode

        self._camera_shake = None

        self._drawHP()

    def _drawHP(self):
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
        jovialengine.shared.font_wrap.renderToInside(
            self._user_interface,
            player_health_dest,
            text_width,
            player_health_text,
            False,
            constants.TEXT_COLOR,
            background=constants.WHITE
        )
        jovialengine.shared.font_wrap.renderToInside(
            self._user_interface,
            enemy_health_dest,
            text_width,
            enemy_health_text,
            False,
            constants.TEXT_COLOR,
            background=constants.WHITE
        )

    def _shakeCamera(self):
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

    def _resetCamera(self):
        self._camera_shake = None
        self._camera.x = 0
        self._camera.y = 0

    def _buttonPress(self):
        self._player_action = self._BOX_CHOICES[self._selected_button]
        self._enemy_action = random.choice(self._enemy_choices)

        if self._player_action == constants.FIGHT_ATTACK:
            self._setActionDisplay("I'm gonna hit 'em!")
            self._player_mon.addWait(self._ANIM_WAIT)
            self._player_mon.addPosRel(jovialengine.AnimSprite.Lerp, 200, 12, 0,
                                       sound=self._thunk, positional_sound=True,
                                       callback=self._shakeCamera)
            self._player_mon.addPosRel(jovialengine.AnimSprite.Lerp, 200, -12, 0)
        elif self._player_action == constants.FIGHT_DEFEND:
            self._setActionDisplay("I'm gonna block 'em!")
            self._player_mon.addWait(self._ANIM_WAIT)
            self._player_mon.addPosRel(jovialengine.AnimSprite.Lerp, 133, -8, 0,
                                       sound=self._bwop, positional_sound=True,
                                       callback=self._shakeCamera)
            self._player_mon.addPosRel(jovialengine.AnimSprite.Lerp, 200, 12, 0)
            self._player_mon.addPosRel(jovialengine.AnimSprite.Lerp, 67, -4, 0)
        elif self._player_action == constants.FIGHT_DODGE:
            self._setActionDisplay("I'm gonna dodge!")
            self._player_mon.addWait(self._ANIM_WAIT)
            self._player_mon.addWait(0, sound=self._rooeee, positional_sound=True)
            self._player_mon.addPosRel(jovialengine.AnimSprite.Lerp, 333, -20, 0)
            self._player_mon.addPosRel(jovialengine.AnimSprite.Lerp, 67, 20, 0)

        if self._enemy_action == constants.FIGHT_ATTACK:
            self._enemy_mon.addWait(self._ANIM_WAIT)
            self._enemy_mon.addPosRel(jovialengine.AnimSprite.Lerp, 200, -12, 0,
                                      sound=self._thunk, positional_sound=True,
                                      callback=self._shakeCamera)
            self._enemy_mon.addPosRel(jovialengine.AnimSprite.Lerp, 200, 12, 0)
        elif self._enemy_action == constants.FIGHT_DEFEND:
            self._enemy_mon.addWait(self._ANIM_WAIT)
            self._enemy_mon.addPosRel(jovialengine.AnimSprite.Lerp, 133, 8, 0,
                                      sound=self._bwop, positional_sound=True,
                                      callback=self._shakeCamera)
            self._enemy_mon.addPosRel(jovialengine.AnimSprite.Lerp, 200, -12, 0)
            self._enemy_mon.addPosRel(jovialengine.AnimSprite.Lerp, 67, 4, 0)
        elif self._enemy_action == constants.FIGHT_DODGE:
            self._enemy_mon.addWait(self._ANIM_WAIT)
            self._enemy_mon.addWait(0, sound=self._rooeee, positional_sound=True)
            self._enemy_mon.addPosRel(jovialengine.AnimSprite.Lerp, 333, 20, 0)
            self._enemy_mon.addPosRel(jovialengine.AnimSprite.Lerp, 67, -20, 0)

    def _input(self, event):
        # click forward to next mode
        if self._result:
            if (event.type == pygame.MOUSEBUTTONUP and event.button == 1) \
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                self._stopMixer()
                jovialengine.shared.state.fight_results.append(self._RESULT_SAVING[self._result])
                self.next_mode = self._get_next_mode()
                return
        # in the middle of action display
        if self._player_action:
            return
        super()._input(event)

    def _setActionDisplay(self, text: str):
        self._action_display.appendleft(
            jovialengine.shared.font_wrap.renderInside(200, text, False, constants.TEXT_COLOR)
        )
        self._action_display_latest = jovialengine.shared.font_wrap.renderInside(200, text, False, constants.BLACK)
        self._action_set = not self._action_set

    def _playerActionDone(self):
        player_hit_block = self._player_mon.fightHit(self._player_action, True)
        enemy_hit_block = self._enemy_mon.fightHit(self._enemy_action)

        raw_player_damage = enemy_hit_block[0] - player_hit_block[1]
        final_player_damage = jovialengine.utility.reduceNumber(
            max(
                0,
                raw_player_damage
            ),
            2
        )
        raw_enemy_damage = player_hit_block[0] - enemy_hit_block[1]
        final_enemy_damage = jovialengine.utility.reduceNumber(
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
        self._setActionDisplay("Hit for " + str(final_enemy_damage) + "! Took " + str(final_player_damage) + "!")
        self._player_mon.stats['hpc'] -= final_player_damage
        self._player_mon.stats['hpc'] = max(self._player_mon.stats['hpc'], 0)
        self._enemy_mon.stats['hpc'] -= final_enemy_damage
        self._enemy_mon.stats['hpc'] = max(self._enemy_mon.stats['hpc'], 0)
        self._drawHP()

        if self._player_mon.stats['hpc'] < 1 and self._enemy_mon.stats['hpc'] < 1:
            self._setupEnd('draw')
        elif self._enemy_mon.stats['hpc'] < 1:
            self._setupEnd('win')
        elif self._player_mon.stats['hpc'] < 1:
            self._setupEnd('lose')
        else:
            self._player_action = False
        self._enemy_action = False

    def _setupEnd(self, ending: str):
        self._player_action = ending
        self._player_mon.addWait(750)
        self._player_mon.addWait(750)
        pygame.mixer.music.fadeout(1000)

    def _update(self, dt):
        if self._camera_shake is not None:
            self._camera_shake -= dt
            if self._camera_shake <= 0:
                self._resetCamera()
        if self._player_action in self._BOX_CHOICES and not self._player_mon.stillAnimating():
            self._playerActionDone()
        elif self._player_action == 'draw':
            self._endStuff("They're both out cold.")
        elif self._player_action == 'win':
            self._endStuff("I won!!!")
        elif self._player_action == 'lose':
            self._endStuff(self._player_mon.name + "'s out cold.")

    def _endStuff(self, result_display: str):
        if len(self._player_mon.anims) < 2 and self._result_displayed < 1:
            self._setActionDisplay(result_display)
            self._result_displayed = 1
        elif not self._player_mon.stillAnimating() and self._result_displayed < 2:
            self._setActionDisplay("Click or press enter to")
            self._setActionDisplay("continue.")
            self._result_displayed = 2
            self._result = self._player_action

    def _updatePreDraw(self, screen):
        screen.fill(constants.WHITE)

    def _drawPreSprites(self, screen):
        screen.blit(self._user_interface, (0, 0))
        if not self._action_set and self._player_action not in self._RESULT_SAVING:
            self._drawSelected(screen)

        player_bar_length = math.ceil(
            self._HEALTH_BAR_LENGTH
            * self._player_mon.stats['hpc'] / self._player_mon.stats['hpm']
        )
        screen.fill(
            self._player_mon.getBarColor(),
            (
                self._PLAYER_BAR_X + 1,
                self._PLAYER_BAR_Y + 1,
                player_bar_length,
                self._HEALTH_BAR_HEIGHT - 2
            )
        )
        screen.fill(
            self._player_mon.getBarColor2(),
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
            self._enemy_mon.getBarColor(),
            (
                self._ENEMY_BAR_X + self._HEALTH_BAR_LENGTH + 1 - enemy_bar_length,
                self._ENEMY_BAR_Y + 1,
                enemy_bar_length,
                self._HEALTH_BAR_HEIGHT - 2
            )
        )
        screen.fill(
            self._enemy_mon.getBarColor2(),
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
