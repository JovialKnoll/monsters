import random
from collections import deque

import pygame

import constants
import shared
import utility
from gamemode import GameMode
from boxes import Boxes

class FightMode(GameMode):
    health_bar_length = 60
    box_choices = [
        "Attack",
        "Defend",
        "Escape",
    ]
    box_rects = (
        pygame.Rect(24,  24,  88,  36),
        pygame.Rect(24,  76,  88,  36),
        pygame.Rect(24, 128,  88,  36),
    )
    boxes = Boxes(
        box_rects,
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
    background = background.convert_alpha(shared.screen)
    black_box = pygame.image.load(constants.BLACKBOX_FILE).convert_alpha(shared.screen)
    health_bar = pygame.image.load(constants.HEALTHBAR_FILE).convert_alpha(shared.screen)

    def __init__(self, player_mon, enemy_mon, draw_mode, win_mode, lose_mode):
        """The functions passed in should return the next mode."""
        super(FightMode, self).__init__()

        player_mon.fightStart()
        self.player_mon = player_mon
        self.enemy_mon = enemy_mon

        self.player_pos = (170,128)
        self.enemy_pos = (262,128)
        self.player_rel = [0,0]
        self.enemy_rel = [0,0]

        self.player_action = False
        self.enemy_action = False
        self.player_anim = 0
        self.enemy_anim = 0

        self.action_display = deque((), 4)
        self.action_set = False

        self.result = False
        self.result_mode = {
            'draw': draw_mode,
            'win': win_mode,
            'lose': lose_mode,
        }

    def _buttonPress(self):
        self.player_action = self.__class__.box_choices[self.__class__.boxes.select]
        self.enemy_action = random.choice(('Attack', 'Defend'))

    def _input(self, event):
        if self.result:
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                self.next_mode = self.result_mode[self.result]()
                return
        if self.player_action:
            return
        if event.type == pygame.MOUSEMOTION:
            self.__class__.boxes.posSelect(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.__class__.boxes.posSelect(event.pos) != None:
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
        damage_to_player = utility.reduceNumber(max( enemy_attack_defend[0] - player_attack_defend[1], 0))
        damage_to_enemy  = utility.reduceNumber(max(player_attack_defend[0] -  enemy_attack_defend[1], 0))
        if damage_to_player == 0 and damage_to_enemy == 0:
            damage_to_player = damage_to_enemy = 1
        # display results below
        self._setActionDisplay("Hit for " + str(damage_to_enemy) + "! Took " + str(damage_to_player) + "!")
        self.player_mon.stats['hpc'] -= damage_to_player
        self.enemy_mon.stats[ 'hpc'] -= damage_to_enemy

        if self.player_mon.stats['hpc'] < 1 and self.enemy_mon.stats['hpc'] < 1:
            self.player_action = 'draw'
        elif self.enemy_mon.stats['hpc'] < 1:
            self.player_action = 'win'
        elif self.player_mon.stats['hpc'] < 1:
            self.player_action = 'lose'
        else:
            self.player_action = False
        self.player_anim = 0
        self.enemy_action = False
        self.enemy_anim = 0

    def update(self):
        # enemy animation
        if self.enemy_action == 'Attack':
            if self.enemy_anim == 0:
                self.enemy_rel[0] -= 1
                if self.enemy_rel[0] == -12:
                    self.enemy_anim = 1
            elif self.enemy_anim == 1:
                self.enemy_rel[0] += 1
                if self.enemy_rel[0] == 0:
                    self.enemy_anim = -1
        elif self.enemy_action == 'Defend':
            if self.enemy_anim == 0:
                self.enemy_rel[0] += 1
                if self.enemy_rel[0] == 8:
                    self.enemy_anim = 1
            elif self.enemy_anim == 1:
                self.enemy_rel[0] -= 1
                if self.enemy_rel[0] == -4:
                    self.enemy_anim = 2
            elif self.enemy_anim == 2:
                self.enemy_rel[0] += 1
                if self.enemy_rel[0] == 0:
                    self.enemy_anim = -1
        # player animation, etc.
        if self.player_action == 'Attack':
            if self.action_set == False:
                self._setActionDisplay("I'm gonna hit 'em!")
            if self.player_anim == 0:
                self.player_rel[0] += 1
                if self.player_rel[0] == 12:
                    self.player_anim = 1
            elif self.player_anim == 1:
                self.player_rel[0] -= 1
                if self.player_rel[0] == 0:
                    self.player_anim = -1
            else:
                self._playerActionDone()
        elif self.player_action == 'Defend':
            if self.action_set == False:
                self._setActionDisplay("I'm gonna block 'em!")
            if self.player_anim == 0:
                self.player_rel[0] -= 1
                if self.player_rel[0] == -8:
                    self.player_anim = 1
            elif self.player_anim == 1:
                self.player_rel[0] += 1
                if self.player_rel[0] == 4:
                    self.player_anim = 2
            elif self.player_anim == 2:
                self.player_rel[0] -= 1
                if self.player_rel[0] == 0:
                    self.player_anim = -1
            else:
                self._playerActionDone()
        elif self.player_action == 'Escape':
            if self.action_set == False:
                self._setActionDisplay("I'm gonna run away!")
            if self.player_anim == 0:
                self.player_rel[0] -= 1
                if self.player_rel[0] == -20:
                    self.player_anim = 1
            elif self.player_anim == 1:
                self.player_rel[0] += 5
                if self.player_rel[0] == 0:
                    self.player_anim = -1
            else:
                self._playerActionDone()
        elif self.player_action == 'draw':
            self._endStuff("They're both out cold.")
        elif self.player_action == 'win':
            self._endStuff("I won!!!")
        elif self.player_action == 'lose':
            self._endStuff(self.player_mon.name + "'s out cold.")

    def _endStuff(self, result_display):
        self.player_anim += 1
        if self.player_anim == 30:
            self._setActionDisplay(result_display)
        elif self.player_anim == 60:
            self._setActionDisplay("Input to continue.")
            self.result = self.player_action

    def _drawScreen(self, screen):
        screen.fill(constants.WHITE)
        screen.blit(self.__class__.background, (0,0))
        if self.action_set == False:
            screen.blit(self.__class__.black_box, self.__class__.boxes.getSelectRect())
        # draw some mons and stuff
        self.player_mon.drawStanding(
            screen,
            (self.player_pos[0] + self.player_rel[0], self.player_pos[1] + self.player_rel[1]),
            True
        )
        player_bar_length = self.__class__.health_bar_length * self.player_mon.stats['hpc'] // self.player_mon.stats['hpm']
        screen.fill(self.player_mon.getLightSkin(), (138, 30, player_bar_length, 10))
        screen.blit(self.__class__.health_bar, (137, 29))

        self.enemy_mon.drawStanding(
            screen,
            (self.enemy_pos[0] + self.enemy_rel[0], self.enemy_pos[1] + self.enemy_rel[1])
        )
        enemy_bar_length = self.__class__.health_bar_length * self.enemy_mon.stats['hpc'] // self.enemy_mon.stats['hpm']
        screen.fill(self.enemy_mon.getLightSkin(), (294-enemy_bar_length, 30, enemy_bar_length, 10))
        screen.blit(self.__class__.health_bar, (233, 29))
        # maybe draw health numbers / stats / etc
        for index, line in enumerate(self.action_display):
            screen.blit(line, (120, 166 - 10 * index))
