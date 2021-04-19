import random
from collections import deque

import pygame

import constants
import shared
import utility
from mode import Mode
from boxes import Boxes
from animsprite import AnimSprite


class ModeFight(Mode):
    health_bar_length = 60
    box_choices = [
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
    for index, choice in enumerate(box_choices):
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

    __slots__ = (
        'thunk',
        'rooeee',
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

    def __init__(self, player_mon, enemy_mon, draw_mode, win_mode, lose_mode):
        """The functions passed in should return the next mode."""
        super().__init__()

        self.thunk = pygame.mixer.Sound(constants.THUNK)
        self.rooeee = pygame.mixer.Sound(constants.ROOEEE)

        self.player_mon = player_mon
        self.enemy_mon = enemy_mon

        self.player_mon.fightStart()
        self.player_mon.setImage(True)

        self.player_mon.rect.midbottom = self.__class__.player_pos
        self.enemy_mon.rect.midbottom = self.__class__.enemy_pos
        self.all_sprites.add(self.player_mon, self.enemy_mon)

        self.player_action = False
        self.enemy_action = False

        self.action_display = deque((), 4)
        self.action_set = False

        self.result_displayed = False

        self.result = False
        self.result_mode = {
            'draw': draw_mode,
            'win': win_mode,
            'lose': lose_mode,
        }

    def _buttonPress(self):
        self.player_action = self.__class__.box_choices[self.__class__.boxes.select]
        self.enemy_action = random.choice(('Attack', 'Defend'))

        if self.player_action == 'Attack':
            self._setActionDisplay("I'm gonna hit 'em!")
            self.player_mon.addPosRel(AnimSprite.Lerp, 200, 12, 0, sound=self.thunk)
            self.player_mon.addPosRel(AnimSprite.Lerp, 200, -12, 0)
        elif self.player_action == 'Defend':
            self._setActionDisplay("I'm gonna block 'em!")
            self.player_mon.addPosRel(AnimSprite.Lerp, 133, -8, 0)
            self.player_mon.addPosRel(AnimSprite.Lerp, 200, 12, 0)
            self.player_mon.addPosRel(AnimSprite.Lerp, 67, -4, 0)
        elif self.player_action == 'Escape':
            self._setActionDisplay("I'm gonna run away!")
            self.player_mon.addWait(0, sound=self.rooeee)
            self.player_mon.addPosRel(AnimSprite.Lerp, 333, -20, 0)
            self.player_mon.addPosRel(AnimSprite.Lerp, 67, 20, 0)

        if self.enemy_action == 'Attack':
            self.enemy_mon.addPosRel(AnimSprite.Lerp, 200, -12, 0, sound=self.thunk)
            self.enemy_mon.addPosRel(AnimSprite.Lerp, 200, 12, 0)
            pass
        elif self.enemy_action == 'Defend':
            self.enemy_mon.addPosRel(AnimSprite.Lerp, 133, 8, 0)
            self.enemy_mon.addPosRel(AnimSprite.Lerp, 200, -12, 0)
            self.enemy_mon.addPosRel(AnimSprite.Lerp, 67, 4, 0)
            pass

    def _input(self, event):
        # click forward to next mode
        if self.result:
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                self.next_mode = self.result_mode[self.result]()
                return
        # in the middle of action display
        if self.player_action:
            return
        if event.type == pygame.MOUSEMOTION:
            self.__class__.boxes.posSelect(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.__class__.boxes.posSelect(event.pos) is not None:
                    self._buttonPress()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._buttonPress()
            # testing stuff, remove later
            elif event.key == pygame.K_t:
                print("player_mon.stats = " + str(self.player_mon.stats))
                print("enemy_mon.stats = " + str(self.enemy_mon.stats))
            else:
                self.__class__.boxes.keySelect(event.key)

    def _setActionDisplay(self, text):
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
            self.player_action = 'draw'
            self.player_mon.addWait(250)
            self.player_mon.addWait(250)
        elif self.enemy_mon.stats['hpc'] < 1:
            self.player_action = 'win'
            self.player_mon.addWait(250)
            self.player_mon.addWait(250)
        elif self.player_mon.stats['hpc'] < 1:
            self.player_action = 'lose'
            self.player_mon.addWait(250)
            self.player_mon.addWait(250)
        else:
            self.player_action = False
        self.enemy_action = False

    def _update(self, dt):
        if self.player_action in self.__class__.box_choices and not self.player_mon.stillAnimating():
            self._playerActionDone()
        elif self.player_action == 'draw':
            self._endStuff("They're both out cold.")
        elif self.player_action == 'win':
            self._endStuff("I won!!!")
        elif self.player_action == 'lose':
            self._endStuff(self.player_mon.name + "'s out cold.")

    def _endStuff(self, result_display):
        if len(self.player_mon.anims) == 1 and not self.result_displayed:
            self._setActionDisplay(result_display)
            self.result_displayed = True
        elif not self.player_mon.stillAnimating:
            self._setActionDisplay("Input to continue.")
            self.result = self.player_action

    def _drawScreen(self, screen):
        screen.fill(constants.WHITE)
        screen.blit(self.__class__.background, (0, 0))
        if not self.action_set:
            screen.blit(self.__class__.black_box, self.__class__.boxes.getSelectRect())

        player_bar_length = self.__class__.health_bar_length \
            * self.player_mon.stats['hpc'] // self.player_mon.stats['hpm']
        screen.fill(self.player_mon.getLightSkin(), (138, 30, player_bar_length, 10))
        screen.blit(self.__class__.health_bar, (137, 29))

        enemy_bar_length = self.__class__.health_bar_length \
            * self.enemy_mon.stats['hpc'] // self.enemy_mon.stats['hpm']
        screen.fill(self.enemy_mon.getLightSkin(), (294 - enemy_bar_length, 30, enemy_bar_length, 10))
        screen.blit(self.__class__.health_bar, (233, 29))
        # maybe draw health numbers / stats / etc
        for index, line in enumerate(self.action_display):
            screen.blit(line, (120, 166 - constants.FONT_HEIGHT * index))
