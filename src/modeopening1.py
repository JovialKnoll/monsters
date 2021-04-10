import pygame

import constants
from mode import Mode
from monster import Monster
from modemonconvo0 import ModeMonConvo0

class ModeOpening1(Mode):
    __slots__ = (
        'left_mon',
        'left_pos',
        'right_mon',
        'right_pos',
    )

    def __init__(self):
        super(ModeOpening1, self).__init__()
        self.left_mon = Monster.atLevel(3)
        self.right_mon = Monster.atLevel(2)
        self.all_sprites.add(self.right_mon, self.left_mon)
        # higher layer = draw later = "in front"
        self.all_sprites.change_layer(self.left_mon, 1)
        self.all_sprites.change_layer(self.right_mon, 0)
        # starts at right
        self.left_mon.rect.bottomright = (constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1] - 32)
        self.left_mon.setImage(True)
        # starts at left
        self.right_mon.rect.bottomleft = (0, constants.SCREEN_SIZE[1] - 32)
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
        self.right_mon.addWait(beat)
        self.right_mon.addPosRel(Monster.Lerp, beat, jump // 2, jump // 2)
        # fire
        self.right_mon.addWait(beat * 2)
        self.right_mon.addPosRel(Monster.Lerp, beat * 1.5, -jump * 6 - jump // 2, -jump * 2 - jump // 2)

    def _changeMode(self):
        self.next_mode = ModeMonConvo0()

    def _input(self, event):
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self._changeMode()

    def _update(self, dt):
        if not self.right_mon.stillAnimating():
            self._changeMode()

    def _drawScreen(self, screen):
        screen.fill(constants.WHITE)
