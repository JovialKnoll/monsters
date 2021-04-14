import random
from collections import deque

import pygame

import constants
import shared
from mode import Mode
from monster import Monster
from modemonconvo0 import ModeMonConvo0

class ModeOpening3(Mode):
    ground_level = constants.SCREEN_SIZE[1] - 16
    center_time = 2500
    transition_time = 750
    empty_time = 250
    full_monster_wait_time = empty_time + transition_time + center_time + transition_time
    initial_wait_time = 0

    __slots__ = (
        'monsters',
        'wait_time',
        'last_level',
        'background',
    )

    def __init__(self):
        super(ModeOpening3, self).__init__()
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
        monster.rect.midbottom = (constants.SCREEN_SIZE[0] // 2, self.__class__.ground_level)
        monster.anims.popleft()
        monster.anims.popleft()
        self.monsters.append(monster)
        self.wait_time = self.__class__.center_time + self.__class__.transition_time
        self.monsters.append(self._getMonster(self.wait_time))
        self.wait_time += self.__class__.full_monster_wait_time
        self.monsters.append(self._getMonster(self.wait_time))
        self.wait_time += self.__class__.full_monster_wait_time
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
            self.__class__.ground_level
        )
        monster.addWait(wait_time + self.__class__.empty_time)
        monster.addPosAbs(
            Monster.Lerp,
            self.__class__.transition_time,
            constants.SCREEN_SIZE[0] // 2,
            self.__class__.ground_level - monster.rect.height // 2
        )
        monster.addWait(self.__class__.center_time)
        monster.addPosAbs(
            Monster.Lerp,
            self.__class__.transition_time,
            monster.rect.width // -2,
            self.__class__.ground_level - monster.rect.height // 2
        )
        return monster

    def _input(self, event):
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self.next_mode = ModeMonConvo0()

    def _update(self, dt):
        self.wait_time -= dt
        # every so often, set up additional looping monsters here, so we don't run out
        if self.wait_time < self.__class__.initial_wait_time - self.__class__.full_monster_wait_time:
            monster = self._getMonster(self.wait_time)
            self.monsters[0].kill()
            self.monsters.append(monster)
            self.wait_time += self.__class__.full_monster_wait_time

    def _drawScreen(self, screen):
        screen.blit(self.background, (0, 0))
