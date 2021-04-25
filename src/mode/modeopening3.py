import random
from collections import deque

import pygame

import constants
import shared
from monster import Monster

from .mode import Mode
from .modemonconvo0 import ModeMonConvo0


class ModeOpening3(Mode):
    GROUND_LEVEL = constants.SCREEN_SIZE[1] - 16
    CENTER_TIME = 2500
    TRANSITION_TIME = 750
    EMPTY_TIME = 250
    FULL_MONSTER_WAIT_TIME = EMPTY_TIME + TRANSITION_TIME + CENTER_TIME + TRANSITION_TIME
    initial_wait_time = 0

    __slots__ = (
        'monsters',
        'wait_time',
        'last_level',
        'background',
    )

    def __init__(self):
        super().__init__()
        # static elements setup
        self.background = pygame.Surface(constants.SCREEN_SIZE).convert(shared.display.screen)
        self.background.fill(constants.WHITE)
        shared.font_wrap.renderToCentered(
            self.background,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 2),
            "press any key to start",
            False,
            constants.BLACK
        )
        # monster loop setup
        self.last_level = random.randint(1, 3)
        self.monsters = deque((), 3)
        monster = self._getMonster(0)
        # start the first one in the center
        monster.rect.midbottom = (constants.SCREEN_SIZE[0] // 2, self.__class__.GROUND_LEVEL)
        monster.anims.popleft()
        monster.anims.popleft()
        self.monsters.append(monster)
        self.wait_time = self.__class__.CENTER_TIME + self.__class__.TRANSITION_TIME
        self.monsters.append(self._getMonster(self.wait_time))
        self.wait_time += self.__class__.FULL_MONSTER_WAIT_TIME
        self.monsters.append(self._getMonster(self.wait_time))
        self.wait_time += self.__class__.FULL_MONSTER_WAIT_TIME
        self.__class__.initial_wait_time = self.wait_time

    def _getMonster(self, wait_time):
        # wait_time is how much time until the previous mon is off the screen
        monster = Monster.atLevel(
            random.choice(
                [i for i in range(1, 4) if i != self.last_level]
            )
        )
        self.last_level = monster.lvl
        self.all_sprites.add(monster)
        monster.rect.midbottom = (
            constants.SCREEN_SIZE[0] + monster.rect.width // 2,
            self.__class__.GROUND_LEVEL
        )
        monster.addWait(wait_time + self.__class__.EMPTY_TIME)
        monster.addPosAbs(
            Monster.Lerp,
            self.__class__.TRANSITION_TIME,
            constants.SCREEN_SIZE[0] // 2,
            self.__class__.GROUND_LEVEL - monster.rect.height // 2
        )
        monster.addWait(self.__class__.CENTER_TIME)
        monster.addPosAbs(
            Monster.Lerp,
            self.__class__.TRANSITION_TIME,
            monster.rect.width // -2,
            self.__class__.GROUND_LEVEL - monster.rect.height // 2
        )
        return monster

    def _input(self, event):
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self._setNextMode(ModeMonConvo0())

    def _update(self, dt):
        self.wait_time -= dt
        # every so often, set up additional looping monsters here, so we don't run out
        if self.wait_time < self.__class__.initial_wait_time - self.__class__.FULL_MONSTER_WAIT_TIME:
            monster = self._getMonster(self.wait_time)
            self.monsters[0].kill()
            self.monsters.append(monster)
            self.wait_time += self.__class__.FULL_MONSTER_WAIT_TIME

    def _drawScreen(self, screen):
        screen.blit(self.background, (0, 0))
