import pygame

import constants
from mode import Mode
from monster import Monster
from modemonconvo0 import ModeMonConvo0

class ModeOpening1(Mode):

    def __init__(self):
        super(ModeOpening1, self).__init__()
        left_mon = Monster.atLevel(3)
        right_mon = Monster.atLevel(2)

        # starts at right
        left_mon.rect.bottomright = (constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1] - 32)
        left_mon.setImage(True)
        # starts at left
        right_mon.rect.bottomleft = (0, constants.SCREEN_SIZE[1] - 32)
        # move to the positions
        beat = 250
        pause = 50
        left_mon.addPosRel(Monster.Lerp, beat * 6, -constants.SCREEN_SIZE[0] // 2, 0)
        right_mon.addPosRel(Monster.Lerp, beat * 6, constants.SCREEN_SIZE[0] // 2, 0)
        # back and forth
        left_mon.addWait(beat * 8 + pause * 2)
        jump = right_mon.rect.width // 8
        right_mon.addPosRel(Monster.Lerp, beat, jump, -jump)
        right_mon.addPosRel(Monster.Lerp, beat, jump, jump)
        right_mon.addPosRel(Monster.Lerp, beat, -jump, -jump)
        right_mon.addPosRel(Monster.Lerp, beat, -jump, jump)
        right_mon.addWait(pause)
        right_mon.addPosRel(Monster.Lerp, beat, jump, -jump)
        right_mon.addPosRel(Monster.Lerp, beat, jump, jump)
        right_mon.addPosRel(Monster.Lerp, beat, -jump, -jump)
        right_mon.addPosRel(Monster.Lerp, beat, -jump, jump)
        right_mon.addWait(pause)
        # small pause
        left_mon.addWait(beat)
        right_mon.addWait(beat)
        # slash!
        left_mon.addPosRel(Monster.Lerp, 100, -jump // 2, -jump // 3)
        left_mon.addPosRel(Monster.Lerp, 200, jump + jump // 2, jump // 3)
        right_mon.addWait(300)
        # jump back
        left_mon.addWait(beat)
        right_mon.addPosRel(Monster.Lerp, beat // 2, jump * 2, -jump * 2)
        right_mon.addPosRel(Monster.Lerp, beat // 2, jump * 2, jump * 2)
        # pause
        left_mon.addWait(150)
        left_mon.addPosRel(Monster.Ler70p, 100, -jump, 0)
        right_mon.addWait(beat)
        # back and forth again
        left_mon.addWait(beat * 4)
        right_mon.addPosRel(Monster.Lerp, beat, -jump, -jump * 2)
        right_mon.addPosRel(Monster.Lerp, beat, -jump, jump * 2)
        right_mon.addPosRel(Monster.Lerp, beat, jump, -jump * 2)
        right_mon.addPosRel(Monster.Lerp, beat, jump, jump * 2)
        # charge
        right_mon.addWait(beat)
        right_mon.addPosRel(Monster.Lerp, beat, jump // 2, jump // 2)
        # fire
        right_mon.addWait(beat * 2)
        right_mon.addPosRel(Monster.Lerp, beat, -jump * 6 - jump // 2, -jump * 2 - jump // 2)

        # higher layer = draw later = "in front"
        left_mon.layer = 1
        right_mon.layer = 0
        self.all_sprites.add(right_mon, left_mon)

    def _changeMode(self):
        self.next_mode = ModeMonConvo0()

    def _input(self, event):
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self._changeMode()

    def _update(self, dt):
        if all(not sprite.stillAnimating() for sprite in self.all_sprites.sprites()):
            self._changeMode()

    def _drawScreen(self, screen):
        screen.fill(constants.WHITE)
