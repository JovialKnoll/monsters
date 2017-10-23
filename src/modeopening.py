import pygame

import constants
from mode import Mode
from monster import Monster
from modeconvo0 import ModeConvo0

class ModeOpening(Mode):
    # next mode: ModeConvo0()
    __slots__ = (
        'left_mon',
        'left_pos',
        'right_mon',
        'right_pos',
    )

    def __init__(self):
        super(ModeOpening, self).__init__()
        self.left_mon = Monster.atLevel(2)
        self.left_pos = [170, 128]
        self.right_mon = Monster.atLevel(2)
        self.right_pos = [262, 128]

    #def _changeMode(self):
    #    self.next_mode = ModeConvo0()

    def _input(self, event):
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self._changeMode()

    def update(self):
        # move positions around
        pass

    def _drawScreen(self, screen):
        screen.fill(constants.WHITE)
        self.left_mon.drawStanding(
            screen,
            self.left_pos,
            True
        )
        self.right_mon.drawStanding(
            screen,
            self.right_pos,
            False
        )
