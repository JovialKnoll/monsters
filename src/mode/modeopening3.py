import random
from collections import deque

import pygame

import constants
import shared
from monster import Monster

from .mode import Mode
from .modemonconvo0 import ModeMonConvo0


class ModeOpening3(Mode):
    GROUND_LEVEL = constants.SCREEN_SIZE[1] - 8
    CENTER_TIME = 2500
    TRANSITION_TIME = 750
    EMPTY_TIME = 250
    FULL_MONSTER_WAIT_TIME = EMPTY_TIME + TRANSITION_TIME + CENTER_TIME + TRANSITION_TIME

    __slots__ = (
        'monsters',
        'wait_time',
        'last_level',
        'background',
        'initial_wait_time',
    )

    def __init__(self):
        super().__init__()
        # static elements setup
        self.background = pygame.Surface(constants.SCREEN_SIZE).convert(shared.display.screen)
        self.background.fill(constants.WHITE)
        shared.font_wrap.renderToCentered(
            self.background,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 2 + 4),
            "press any key to start",
            False,
            constants.BLACK
        )
        logo = pygame.image.load(constants.CHIKKAI_LOGO).convert(shared.display.screen)
        self.background.blit(
            logo,
            (
                constants.SCREEN_SIZE[0] // 2 - logo.get_width() // 2,
                constants.SCREEN_SIZE[1] // 4 - logo.get_height() // 2,
            )
        )
        # monster loop setup
        self.last_level = 3
        self.monsters = deque((), 3)
        monster = self._getMonster(0, 3)
        # start the first one in the center
        monster.rect.midbottom = (constants.SCREEN_SIZE[0] // 2, self.GROUND_LEVEL)
        monster.anims.popleft()
        monster.anims.popleft()
        self.monsters.append(monster)
        self.wait_time = self.CENTER_TIME + self.TRANSITION_TIME
        self.monsters.append(self._getMonster(self.wait_time))
        self.wait_time += self.FULL_MONSTER_WAIT_TIME
        self.monsters.append(self._getMonster(self.wait_time))
        self.wait_time += self.FULL_MONSTER_WAIT_TIME
        self.initial_wait_time = self.wait_time

    def _getMonster(self, wait_time, level=None):
        # wait_time is how much time until the previous mon is off the screen
        if level is None:
            level = random.choice(
                [i for i in range(1, 4) if i != self.last_level]
            )
        monster = Monster.atLevel(level)
        self.last_level = level
        self.all_sprites.add(monster)
        monster.rect.midbottom = (
            constants.SCREEN_SIZE[0] + monster.rect.width // 2,
            self.GROUND_LEVEL
        )
        monster.addWait(wait_time + self.EMPTY_TIME)
        monster.addPosAbs(
            Monster.Lerp,
            self.TRANSITION_TIME,
            constants.SCREEN_SIZE[0] // 2,
            self.GROUND_LEVEL - monster.rect.height // 2
        )
        monster.addWait(self.CENTER_TIME)
        monster.addPosAbs(
            Monster.Lerp,
            self.TRANSITION_TIME,
            monster.rect.width // -2,
            self.GROUND_LEVEL - monster.rect.height // 2
        )
        return monster

    def _input(self, event):
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self._stopMixer()
            self.next_mode = ModeMonConvo0()

    def _update(self, dt):
        self.wait_time -= dt
        # every so often, set up additional looping monsters here, so we don't run out
        if self.wait_time < self.initial_wait_time - self.FULL_MONSTER_WAIT_TIME:
            monster = self._getMonster(self.wait_time)
            self.monsters[0].kill()
            self.monsters.append(monster)
            self.wait_time += self.FULL_MONSTER_WAIT_TIME

    def _drawScreen(self, screen):
        screen.blit(self.background, (0, 0))
