import random
from collections import deque

import pygame
import jovialengine

import constants
from monster import Monster
from .modeintroduction0 import ModeIntroduction0
from .modeopening import ModeOpening


class ModeOpening3(ModeOpening):
    _GROUND_LEVEL = constants.SCREEN_SIZE[1] - 8
    _CENTER_TIME = 1500
    _TRANSITION_TIME = 500
    _EMPTY_TIME = 100
    _FULL_MONSTER_WAIT_TIME = _EMPTY_TIME + _TRANSITION_TIME + _CENTER_TIME + _TRANSITION_TIME

    __slots__ = (
        '_monsters',
        '_wait_time',
        '_last_level',
        '_initial_wait_time',
    )

    def __init__(self):
        super().__init__()
        # static elements setup
        self._background.fill(constants.WHITE)
        jovialengine.shared.font_wrap.renderToCentered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 2 + 4),
            "press any key to start",
            False,
            constants.BLACK
        )
        logo = pygame.image.load(constants.CHIKKAI_LOGO).convert()
        self._background.blit(
            logo,
            (
                constants.SCREEN_SIZE[0] // 2 - logo.get_width() // 2,
                constants.SCREEN_SIZE[1] // 4 - logo.get_height() // 2,
            )
        )
        version_width = len(constants.VERSION) * constants.FONT_SIZE
        jovialengine.shared.font_wrap.renderToInside(
            self._background,
            (constants.SCREEN_SIZE[0] - version_width, constants.SCREEN_SIZE[1] - constants.FONT_HEIGHT),
            version_width,
            constants.VERSION,
            False,
            constants.TEXT_COLOR
        )
        # monster loop setup
        self._last_level = 3
        self._monsters = deque((), 3)
        monster = self._getMonster(0, 3)
        # start the first one in the center
        monster.rect.midbottom = (constants.SCREEN_SIZE[0] // 2, self._GROUND_LEVEL)
        monster.anims.popleft()
        monster.anims.popleft()
        self._monsters.append(monster)
        self._wait_time = self._CENTER_TIME + self._TRANSITION_TIME
        self._monsters.append(self._getMonster(self._wait_time))
        self._wait_time += self._FULL_MONSTER_WAIT_TIME
        self._monsters.append(self._getMonster(self._wait_time))
        self._wait_time += self._FULL_MONSTER_WAIT_TIME
        self._initial_wait_time = self._wait_time

    def _getMonster(self, _wait_time, level=None):
        # _wait_time is how much time until the previous mon is off the screen
        if level is None:
            level = random.choice(
                [i for i in range(1, 4) if i != self._last_level]
            )
        monster = Monster.atLevel(level)
        self._last_level = level
        self._all_sprites.add(monster)
        monster.rect.midbottom = (
            constants.SCREEN_SIZE[0] + monster.rect.width // 2,
            self._GROUND_LEVEL
        )
        monster.addWait(_wait_time + self._EMPTY_TIME)
        monster.addPosAbs(
            Monster.Lerp,
            self._TRANSITION_TIME,
            constants.SCREEN_SIZE[0] // 2,
            self._GROUND_LEVEL - monster.rect.height // 2
        )
        monster.addWait(self._CENTER_TIME)
        monster.addPosAbs(
            Monster.Lerp,
            self._TRANSITION_TIME,
            monster.rect.width // -2,
            self._GROUND_LEVEL - monster.rect.height // 2
        )
        return monster

    def _switchMode(self):
        self.next_mode = ModeIntroduction0()

    def _update(self, dt):
        self._wait_time -= dt
        # every so often, set up additional looping _monsters here, so we don't run out
        if self._wait_time < self._initial_wait_time - self._FULL_MONSTER_WAIT_TIME:
            monster = self._getMonster(self._wait_time)
            self._monsters[0].kill()
            self._monsters.append(monster)
            self._wait_time += self._FULL_MONSTER_WAIT_TIME
