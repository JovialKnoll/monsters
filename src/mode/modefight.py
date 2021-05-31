import random
from collections import deque

import pygame

import constants
import shared
import utility
from animsprite import AnimSprite
from monster import Monster

from .mode import Mode
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
    _health_bar = pygame.image.load(constants.HEALTHBAR_FILE).convert(shared.display.screen)
    _health_bar.set_colorkey(constants.COLORKEY)
    _PLAYER_POS = (170, 128)
    _ENEMY_POS = (262, 128)
    _ANIM_WAIT = 250
    _HEALTH_BAR_LENGTH = 60
    _BOX_CHOICES = [
        "Attack",
        "Defend",
        "Escape",
    ]

    __slots__ = (
        'background',
        'thunk',
        'rooeee',
        'bwop',
        'player_mon',
        'enemy_mon',
        'player_action',
        'enemy_action',
        'action_display',
        'action_set',
        'result_displayed',
        'result',
        'result_mode',
    )

    def __init__(self, player_mon: Monster, enemy_mon: Monster, draw_mode: Mode, win_mode: Mode, lose_mode: Mode):
        """The functions passed in should return the next mode."""
        super().__init__()

        self.background = pygame.image.load(constants.LAYOUT_2_FILE)
        for index, choice in enumerate(self._BOX_CHOICES):
            shared.font_wrap.renderToInside(
                self.background,
                self.textStart(index),
                self.textWidth(index),
                choice,
                False,
                constants.TEXT_COLOR
            )
        self.background = self.background.convert(shared.display.screen)
        self.background.set_colorkey(constants.COLORKEY)

        pygame.mixer.music.load(constants.FIGHT_LOOP)
        pygame.mixer.music.play(-1)

        self.thunk = pygame.mixer.Sound(constants.THUNK)
        self.rooeee = pygame.mixer.Sound(constants.ROOEEE)
        self.bwop = pygame.mixer.Sound(constants.BWOP)

        self.player_mon = player_mon
        self.enemy_mon = enemy_mon

        self.player_mon.fightStart()
        self.player_mon.setImage(True)

        self.player_mon.rect.midbottom = self._PLAYER_POS
        self.enemy_mon.rect.midbottom = self._ENEMY_POS
        self.all_sprites.add(self.player_mon, self.enemy_mon)

        self.player_action = False
        self.enemy_action = False

        self.action_display = deque((), 4)
        self.action_set = False

        self.result_displayed = 0

        self.result = False
        self.result_mode = {
            'draw': draw_mode,
            'win': win_mode,
            'lose': lose_mode,
        }

    def _buttonPress(self):
        print(self.player_mon.rect.midbottom)
        self.player_action = self._BOX_CHOICES[self._selected_button]
        self.enemy_action = random.choice(('Attack', 'Defend'))

        if self.player_action == 'Attack':
            self._setActionDisplay("I'm gonna hit 'em!")
            self.player_mon.addWait(self._ANIM_WAIT)
            self.player_mon.addPosRel(AnimSprite.Lerp, 200, 12, 0, sound=self.thunk)
            self.player_mon.addPosRel(AnimSprite.Lerp, 200, -12, 0)
        elif self.player_action == 'Defend':
            self._setActionDisplay("I'm gonna block 'em!")
            self.player_mon.addWait(self._ANIM_WAIT)
            self.player_mon.addPosRel(AnimSprite.Lerp, 133, -8, 0, sound=self.bwop)
            self.player_mon.addPosRel(AnimSprite.Lerp, 200, 12, 0)
            self.player_mon.addPosRel(AnimSprite.Lerp, 67, -4, 0)
        elif self.player_action == 'Escape':
            self._setActionDisplay("I'm gonna run away!")
            self.player_mon.addWait(self._ANIM_WAIT)
            self.player_mon.addWait(0, sound=self.rooeee)
            self.player_mon.addPosRel(AnimSprite.Lerp, 333, -20, 0)
            self.player_mon.addPosRel(AnimSprite.Lerp, 67, 20, 0)

        if self.enemy_action == 'Attack':
            self.enemy_mon.addWait(self._ANIM_WAIT)
            self.enemy_mon.addPosRel(AnimSprite.Lerp, 200, -12, 0, sound=self.thunk)
            self.enemy_mon.addPosRel(AnimSprite.Lerp, 200, 12, 0)
            pass
        elif self.enemy_action == 'Defend':
            self.enemy_mon.addWait(self._ANIM_WAIT)
            self.enemy_mon.addPosRel(AnimSprite.Lerp, 133, 8, 0, sound=self.bwop)
            self.enemy_mon.addPosRel(AnimSprite.Lerp, 200, -12, 0)
            self.enemy_mon.addPosRel(AnimSprite.Lerp, 67, 4, 0)
            pass

    def _input(self, event):
        # click forward to next mode
        if self.result:
            if (event.type == pygame.MOUSEBUTTONUP and event.button == 1) \
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                self._stopMixer()
                self.next_mode = self.result_mode[self.result]()
                return
        # in the middle of action display
        if self.player_action:
            return
        if event.type == pygame.MOUSEMOTION:
            self.posSelect(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.posSelect(event.pos) is not None \
                    and self._mouseButtonStatus(event.button) \
                    and self.posSelect(self._mouseButtonStatus(event.button)) \
                        == self.posSelect(event.pos):
                    self._buttonPress()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._buttonPress()
            # testing stuff, remove later
            elif event.key == pygame.K_t:
                print("player_mon.stats = " + str(self.player_mon.stats))
                print("enemy_mon.stats = " + str(self.enemy_mon.stats))
            else:
                self.keySelect(event.key)

    def _setActionDisplay(self, text: str):
        self.action_display.appendleft(shared.font_wrap.renderInside(200, text, False, constants.TEXT_COLOR))
        self.action_set = not self.action_set

    def _playerActionDone(self):
        player_attack_defend = self.player_mon.fightHit(self.player_action)
        enemy_attack_defend = self.enemy_mon.fightHit(self.enemy_action)
        # print "player_attack_defend = " + str(player_attack_defend)
        # print "enemy_attack_defend  = " + str(enemy_attack_defend)
        damage_to_player = utility.reduceNumber(
            max(
                0,
                enemy_attack_defend[0] - player_attack_defend[1]
            ),
            2
        )
        damage_to_enemy = utility.reduceNumber(
            max(
                0,
                player_attack_defend[0] - enemy_attack_defend[1]
            ),
            2
        )
        if damage_to_player == 0 and damage_to_enemy == 0:
            damage_to_player = damage_to_enemy = 1
        # display results below
        self._setActionDisplay("Hit for " + str(damage_to_enemy) + "! Took " + str(damage_to_player) + "!")
        self.player_mon.stats['hpc'] -= damage_to_player
        self.enemy_mon.stats['hpc'] -= damage_to_enemy

        if self.player_mon.stats['hpc'] < 1 and self.enemy_mon.stats['hpc'] < 1:
            self._setupEnd('draw')
        elif self.enemy_mon.stats['hpc'] < 1:
            self._setupEnd('win')
        elif self.player_mon.stats['hpc'] < 1:
            self._setupEnd('lose')
        else:
            self.player_action = False
        self.enemy_action = False

    def _setupEnd(self, ending: str):
        self.player_action = ending
        self.player_mon.addWait(500)
        self.player_mon.addWait(500)
        pygame.mixer.music.fadeout(1000)

    def _update(self, dt):
        if self.player_action in self._BOX_CHOICES and not self.player_mon.stillAnimating():
            self._playerActionDone()
        elif self.player_action == 'draw':
            self._endStuff("They're both out cold.")
        elif self.player_action == 'win':
            self._endStuff("I won!!!")
        elif self.player_action == 'lose':
            self._endStuff(self.player_mon.name + "'s out cold.")

    def _endStuff(self, result_display: str):
        if len(self.player_mon.anims) < 2 and self.result_displayed < 1:
            self._setActionDisplay(result_display)
            self.result_displayed = 1
        elif not self.player_mon.stillAnimating() and self.result_displayed < 2:
            self._setActionDisplay("Click or press enter to")
            self._setActionDisplay("continue.")
            self.result_displayed = 2
            self.result = self.player_action

    def _drawScreen(self, screen):
        screen.fill(constants.WHITE)
        screen.blit(self.background, (0, 0))
        if not self.action_set and self.player_action not in self.result_mode:
            self.drawSelected(screen)

        player_bar_length = self._HEALTH_BAR_LENGTH \
            * self.player_mon.stats['hpc'] // self.player_mon.stats['hpm']
        screen.fill(self.player_mon.getLightSkin(), (138, 30, player_bar_length, 10))
        screen.blit(self._health_bar, (137, 29))

        enemy_bar_length = self._HEALTH_BAR_LENGTH \
            * self.enemy_mon.stats['hpc'] // self.enemy_mon.stats['hpm']
        screen.fill(self.enemy_mon.getLightSkin(), (294 - enemy_bar_length, 30, enemy_bar_length, 10))
        screen.blit(self._health_bar, (233, 29))
        # maybe draw health numbers / stats / etc
        for index, line in enumerate(self.action_display):
            screen.blit(line, (120, 166 - constants.FONT_HEIGHT * index))
