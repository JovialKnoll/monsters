from collections import deque

import pygame

import utility
from anim import Anim

class AnimSprite(pygame.sprite.Sprite):
    Lerp = 'LERP'
    IncSpeed = 'INC_SPEED'
    DecSpeed = 'DEC_SPEED'
    IncDecSpeed = 'INC_DEC_SPEED'
    DecIncSpeed = 'DEC_INC_SPEED'
    funcDict = {
        Lerp: utility.lerp,
        IncSpeed: utility.incSpeedLerp,
        DecSpeed: utility.decSpeedLerp,
        IncDecSpeed: utility.incDecSpeedLerp,
        DecIncSpeed: utility.decIncSpeedLerp,
    }
    @classmethod
    def toFunc(cls, type):
        return funcDict.get(type, utility.lerp)

    __slots__ = (
        'anims',
        'last_pos',
        'time',
    )
    def __getstate__(self):
        return (self.rect, self.anims, last_pos, time)
    def __setstate__(self, state):
        super(AnimSprite, self).__init__()
        self.rect, self.anims, self.last_pos, self.time = state

    def __init__(self):
        super(AnimSprite, self).__init__()
        self.anims = deque()
        self.last_pos = None
        self.time = 0

    def update(self, *args):
        if self.last_pos is None:
            self.last_pos = self.rect.topleft
        # adding dt
        self.time += args[0]
        while self.anims and self.time >= self.anims[-1].time:
            done_anim = self.anims.pop()
            self.time -= done_anim.time
            self.rect.topleft = done_anim.pos
            self.last_pos = self.rect.topleft
        if self.anims:
            current_anim = self.anims[-1]
            func = self.__class__.toFunc(current_anim.type)
            self.rect.topleft = func(
                self.last_pos,
                current_anim.pos,
                self.time / current_anim.time
            )
        else:
            self.time = 0

    def addPosAbs(self, type, time, x_or_pair, y = None):
        self.anims.appendleft(
            Anim(type, time, x_or_pair, y)
        )

    def addPosRel(self, type, time, x_or_pair, y = None):
        newPos = Vec2d(x_or_pair, y)
        if self.anims:
            newPos += anims[0].pos
        else:
            newPos += self.rect.topleft
        self.addPosAbs(type, time, newPos)
