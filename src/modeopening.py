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
        # set monsters
        self.left_mon = Monster.atLevel(2)
        self.right_mon = Monster.atLevel(2)
        # set positions
        self.left_mon.rect.midbottom = (170, 128)
        self.left_mon.setImage(True)
        self.right_mon.rect.midbottom = (262, 128)
        # set animations
        self.left_mon.addPosRel(Monster.Lerp, 2000, -50, 0)
        self.left_mon.addPosRel(Monster.IncSpeed, 2000, 0, -50)
        self.left_mon.addPosRel(Monster.DecSpeed, 3000, 50, 50)
        self.left_mon.addPosAbs(Monster.IncDecSpeed, 4000, 0, 0)
        self.left_mon.addPosAbs(Monster.DecIncSpeed, 4000, 100, 100)
        # add to all_sprites
        self.all_sprites.add(self.left_mon, self.right_mon)

    def _changeMode(self):
        self.next_mode = ModeConvo0()

    def _input(self, event):
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self._changeMode()

    def _drawScreen(self, screen):
        screen.fill(constants.WHITE)
