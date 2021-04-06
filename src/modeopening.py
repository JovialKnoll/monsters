import pygame

import constants
from mode import Mode
from monster import Monster
from modeconvo0 import ModeConvo0
from modetest import ModeTest

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
        # higher layer = draw later = "in front"
        self.left_mon._layer = 1
        self.right_mon._layer = 0
        self.all_sprites.add(self.right_mon, self.left_mon)
        # starts at right
        self.left_mon.rect.bottomright = constants.SCREEN_SIZE
        self.left_mon.setImage(True)
        # starts at left
        self.right_mon.rect.bottomleft = (0, constants.SCREEN_SIZE[1])
        # move to the positions
        beat = 250
        pause = 50
        self.left_mon.addPosRel(Monster.Lerp, beat * 6, -constants.SCREEN_SIZE[0] // 2, 0)
        self.right_mon.addPosRel(Monster.Lerp, beat * 6, constants.SCREEN_SIZE[0] // 2, 0)
        # back and forth
        self.left_mon.addWait(beat * 8 + pause * 2)
        jump = self.right_mon.rect.width // 8
        self.right_mon.addPosRel(Monster.Lerp, beat, jump, -jump)
        self.right_mon.addPosRel(Monster.Lerp, beat, jump, jump)
        self.right_mon.addPosRel(Monster.Lerp, beat, -jump, -jump)
        self.right_mon.addPosRel(Monster.Lerp, beat, -jump, jump)
        self.right_mon.addWait(pause)
        self.right_mon.addPosRel(Monster.Lerp, beat, jump, -jump)
        self.right_mon.addPosRel(Monster.Lerp, beat, jump, jump)
        self.right_mon.addPosRel(Monster.Lerp, beat, -jump, -jump)
        self.right_mon.addPosRel(Monster.Lerp, beat, -jump, jump)
        self.right_mon.addWait(pause)
        # small pause
        self.left_mon.addWait(beat)
        self.right_mon.addWait(beat)
        # slash!
        self.left_mon.addPosRel(Monster.Lerp, 100, -jump // 2, -jump // 3)
        self.left_mon.addPosRel(Monster.Lerp, 200, jump + jump // 2, jump // 3)
        self.right_mon.addWait(300)
        # jump back
        self.left_mon.addWait(beat)
        self.right_mon.addPosRel(Monster.Lerp, beat // 2, jump * 2, -jump * 2)
        self.right_mon.addPosRel(Monster.Lerp, beat // 2, jump * 2, jump * 2)
        # pause
        self.left_mon.addWait(150)
        self.left_mon.addPosRel(Monster.Lerp, 100, -jump, 0)
        self.right_mon.addWait(beat)
        # back and forth again
        self.left_mon.addWait(beat * 4)
        self.right_mon.addPosRel(Monster.Lerp, beat, -jump, -jump * 2)
        self.right_mon.addPosRel(Monster.Lerp, beat, -jump, jump * 2)
        self.right_mon.addPosRel(Monster.Lerp, beat, jump, -jump * 2)
        self.right_mon.addPosRel(Monster.Lerp, beat, jump, jump * 2)
        # charge
        # self.left_mon.addWait(beat)
        # self.right_mon.addPosRel(Monster.Lerp, beat, -jump, -jump * 2)
        # fire
    def _changeMode(self):
        self.next_mode = ModeTest()

    def _input(self, event):
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self._changeMode()

    def _drawScreen(self, screen):
        screen.fill(constants.WHITE)
