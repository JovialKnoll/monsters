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
        self.left_mon = Monster.atLevel(3)
        self.right_mon = Monster.atLevel(2)
        # starts at right
        self.left_mon.rect.bottomright = constants.SCREEN_SIZE
        self.left_mon.setImage(True)
        # starts at left
        self.right_mon.rect.bottomleft = (0, constants.SCREEN_SIZE[1])
        # move to the positions
        self.left_mon.addPosRel(Monster.Lerp, 250 * 6, -constants.SCREEN_SIZE[0] // 2, 0)
        self.right_mon.addPosRel(Monster.Lerp, 250 * 6, constants.SCREEN_SIZE[0] // 2, 0)
        # back and forth
        self.left_mon.addWait(250 * 8 + 50 * 2)
        jump = self.right_mon.rect.width // 8
        self.right_mon.addPosRel(Monster.Lerp, 250, jump, -jump)
        self.right_mon.addPosRel(Monster.Lerp, 250, jump, jump)
        self.right_mon.addPosRel(Monster.Lerp, 250, -jump, -jump)
        self.right_mon.addPosRel(Monster.Lerp, 250, -jump, jump)
        self.right_mon.addWait(50)
        self.right_mon.addPosRel(Monster.Lerp, 250, jump, -jump)
        self.right_mon.addPosRel(Monster.Lerp, 250, jump, jump)
        self.right_mon.addPosRel(Monster.Lerp, 250, -jump, -jump)
        self.right_mon.addPosRel(Monster.Lerp, 250, -jump, jump)
        self.right_mon.addWait(50)
        # small pause
        self.left_mon.addWait(250)
        self.right_mon.addWait(250)
        # slash!
        self.left_mon.addPosRel(Monster.Lerp, 100, -jump // 2, -jump // 3)
        self.left_mon.addPosRel(Monster.Lerp, 200, jump + jump // 2, jump // 3)
        self.right_mon.addWait(300)
        # jump back
        self.left_mon.addWait(250)
        self.right_mon.addPosRel(Monster.Lerp, 125, jump, -jump * 2)
        self.right_mon.addPosRel(Monster.Lerp, 125, jump, jump * 2)
        # pause
        self.left_mon.addWait(150)
        self.left_mon.addPosRel(Monster.Lerp, 100, -jump, 0)
        self.right_mon.addWait(250)
        # back and forth again
        self.left_mon.addWait(250 * 4)
        self.right_mon.addPosRel(Monster.Lerp, 250, -jump, -jump * 2)
        self.right_mon.addPosRel(Monster.Lerp, 250, -jump, jump * 2)
        self.right_mon.addPosRel(Monster.Lerp, 250, jump, -jump * 2)
        self.right_mon.addPosRel(Monster.Lerp, 250, jump, jump * 2)
        # add to all_sprites
        self.all_sprites.add(self.right_mon, self.left_mon)

    def _changeMode(self):
        self.next_mode = ModeConvo0()

    def _input(self, event):
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self._changeMode()

    def _drawScreen(self, screen):
        screen.fill(constants.WHITE)
