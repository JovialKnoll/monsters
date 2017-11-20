from collections import deque

import pygame

import utility
from anim import Anim
from vec2d import Vec2d

class AnimSprite(pygame.sprite.DirtySprite):
    Binary = 'Binary'
    Lerp = 'LERP'
    IncSpeed = 'INC'
    DecSpeed = 'DEC'
    IncDecSpeed = 'INC_DEC'
    DecIncSpeed = 'DEC_INC'
    funcDict = {
        Binary: utility.binary,
        Lerp: utility.lerp,
        IncSpeed: utility.incSpeedLerp,
        DecSpeed: utility.decSpeedLerp,
        IncDecSpeed: utility.incDecSpeedLerp,
        DecIncSpeed: utility.decIncSpeedLerp,
    }
    @classmethod
    def toFunc(cls, func):
        return cls.funcDict.get(func, utility.lerp)

    __slots__ = (
        'anims',
        'last_pos',
        'time',
    )
    def __getstate__(self):
        return (self.rect, self.anims, self.last_pos, self.time)
    def __setstate__(self, state):
        super(AnimSprite, self).__init__()
        self.rect, self.anims, self.last_pos, self.time = state

    def __init__(self):
        super(AnimSprite, self).__init__()
        # dirty = 2 : always draw
        self.dirty = 2
        self.anims = deque()
        self.last_pos = None
        self.time = 0

    def stillAnimating(self):
        if self.anims:
            return True
        return False

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
            func = self.__class__.toFunc(current_anim.func)
            self.rect.topleft = func(
                self.last_pos,
                current_anim.pos,
                self.time / current_anim.time
            )
        else:
            self.time = 0

    def addPosAbs(self, func, time, x_or_pair, y=None):
        self.anims.appendleft(
            Anim(func, time, x_or_pair, y)
        )

    def addPosRel(self, func, time, x_or_pair, y=None):
        newPos = Vec2d(x_or_pair, y)
        if self.anims:
            newPos += self.anims[0].pos
        else:
            newPos += self.rect.topleft
        self.addPosAbs(func, time, newPos)

    def addWait(self, time):
        self.addPosRel(AnimSprite.Binary, time, 0, 0)
