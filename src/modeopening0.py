import pygame

import constants
from mode import Mode
from modeopening1 import ModeOpening1

class ModeOpening0(Mode):
    __slots__ = (
    )

    def __init__(self):
        super(ModeOpening0, self).__init__()

    def _changeMode(self):
        self.next_mode = ModeOpening1()

    def _input(self, event):
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self._changeMode()

    def _update(self, dt):
        pass
        # if not self.right_mon.stillAnimating():
        #     self._changeMode()

    def _drawScreen(self, screen):
        screen.fill(constants.BLACK)
