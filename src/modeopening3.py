from collections import deque

import pygame

import constants
from mode import Mode
from monster import Monster
from modemonconvo0 import ModeMonConvo0

class ModeOpening3(Mode):

    __slots__ = (
        'monsters'
    )

    def __init__(self):
        super(ModeOpening3, self).__init__()
        # set up title display here
        self.monsters = deque((), 3)
        # set up looping monsters here

    def _addLoopMonster(self):
        pass

    def _input(self, event):
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self.next_mode = ModeMonConvo0()

    def _update(self, dt):
        # every so often, set up additional looping monsters here, so we don't run out
        # also remove old monsters from self.all_sprites
        pass

    def _drawScreen(self, screen):
        screen.fill(constants.WHITE)
