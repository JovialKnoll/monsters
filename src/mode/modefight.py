import random
from collections import deque

import pygame

import constants
import shared
import utility
from boxes import Boxes
from animsprite import AnimSprite
from monster import Monster

from .mode import Mode


class ModeFight(Mode):
    HEALTH_BAR_LENGTH = 60
    BOX_CHOICES = [
        "Attack",
        "Defend",
        "Escape",
    ]
    boxes = Boxes(
        (
            pygame.Rect(24, 24, 88, 36),
            pygame.Rect(24, 76, 88, 36),
            pygame.Rect(24, 128, 88, 36),
        ),
        (
            pygame.K_UP,
            pygame.K_LEFT,
        ),
        (
            pygame.K_DOWN,
            pygame.K_RIGHT,
        )
    )
    background = pygame.image.load(constants.LAYOUT_2_FILE)
    for index, choice in enumerate(BOX_CHOICES):
        shared.font_wrap.renderToInside(
            background,
            boxes.textStart(index),
            boxes.textWidth(index),
            choice,
            False,
            constants.TEXT_COLOR
        )
    background = background.convert(shared.display.screen)
    background.set_colorkey(constants.COLORKEY)
    black_box = pygame.image.load(constants.BLACKBOX_FILE).convert(shared.display.screen)
    black_box.set_colorkey(constants.COLORKEY)
    health_bar = pygame.image.load(constants.HEALTHBAR_FILE).convert(shared.display.screen)
    health_bar.set_colorkey(constants.COLORKEY)
    player_pos = (170, 128)
    enemy_pos = (262, 128)
    anim_wait = 250

    __slots__ = (
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

        print("start music")
        pygame.mixer.music.load(constants.FIGHT_LOOP)
        pygame.mixer.music.play(-1)

        self.thunk = pygame.mixer.Sound(constants.THUNK)
        self.rooeee = pygame.mixer.Sound(constants.ROOEEE)
        self.bwop = pygame.mixer.Sound(constants.BWOP)

        self.player_mon = player_mon
        self.enemy_mon = enemy_mon

        self.player_mon.fightStart()
        self.player_mon.setImage(True)

        self.player_mon.rect.midbottom = self.player_pos
        self.enemy_mon.rect.midbottom = self.enemy_pos
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
        self.player_action = self.BOX_CHOICES[self.boxes.select]
        self.enemy_action = random.choice(('Attack', 'Defend'))

        if self.player_action == 'Attack':
            self._setActionDisplay("I'm gonna hit 'em!")
            self.player_mon.addWait(self.anim_wait)
            self.player_mon.addPosRel(AnimSprite.Lerp, 200, 12, 0, sound=self.thunk)
            self.player_mon.addPosRel(AnimSprite.Lerp, 200, -12, 0)
        elif self.player_action == 'Defend':
            self._setActionDisplay("I'm gonna block 'em!")
            self.player_mon.addWait(self.anim_wait)
            self.player_mon.addPosRel(AnimSprite.Lerp, 133, -8, 0, sound=self.bwop)
            self.player_mon.addPosRel(AnimSprite.Lerp, 200, 12, 0)
            self.player_mon.addPosRel(AnimSprite.Lerp, 67, -4, 0)
        elif self.player_action == 'Escape':
            self._setActionDisplay("I'm gonna run away!")
            self.player_mon.addWait(self.anim_wait)
            self.player_mon.addWait(0, sound=self.rooeee)
            self.player_mon.addPosRel(AnimSprite.Lerp, 333, -20, 0)
            self.player_mon.addPosRel(AnimSprite.Lerp, 67, 20, 0)

        if self.enemy_action == 'Attack':
            self.enemy_mon.addWait(self.anim_wait)
            self.enemy_mon.addPosRel(AnimSprite.Lerp, 200, -12, 0, sound=self.thunk)
            self.enemy_mon.addPosRel(AnimSprite.Lerp, 200, 12, 0)
            pass
        elif self.enemy_action == 'Defend':
            self.enemy_mon.addWait(self.anim_wait)
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
            self.boxes.posSelect(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.boxes.posSelect(event.pos) is not None \
                    and self._mouseButtonStatus(event.button) \
                    and self.boxes.posSelect(self._mouseButtonStatus(event.button)) \
                        == self.boxes.posSelect(event.pos):
                    self._buttonPress()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._buttonPress()
            # testing stuff, remove later
            elif event.key == pygame.K_t:
                print("player_mon.stats = " + str(self.player_mon.stats))
                print("enemy_mon.stats = " + str(self.enemy_mon.stats))
            else:
                self.boxes.keySelect(event.key)

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
        if self.player_action in self.BOX_CHOICES and not self.player_mon.stillAnimating():
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
            screen.blit(self.black_box, self.boxes.getSelectRect())

        player_bar_length = self.HEALTH_BAR_LENGTH \
            * self.player_mon.stats['hpc'] // self.player_mon.stats['hpm']
        screen.fill(self.player_mon.getLightSkin(), (138, 30, player_bar_length, 10))
        screen.blit(self.health_bar, (137, 29))

        enemy_bar_length = self.HEALTH_BAR_LENGTH \
            * self.enemy_mon.stats['hpc'] // self.enemy_mon.stats['hpm']
        screen.fill(self.enemy_mon.getLightSkin(), (294 - enemy_bar_length, 30, enemy_bar_length, 10))
        screen.blit(self.health_bar, (233, 29))
        # maybe draw health numbers / stats / etc
        for index, line in enumerate(self.action_display):
            screen.blit(line, (120, 166 - constants.FONT_HEIGHT * index))
