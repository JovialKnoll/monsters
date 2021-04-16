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
        super().__init__()
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
            self.last_pos = self.rect.center
        # adding dt
        self.time += args[0]
        while self.anims and self.time >= self.anims[0].time:
            done_anim = self.anims.popleft()
            if (done_anim.sound):
                done_anim.sound.play()
            self.time -= done_anim.time
            self.rect.center = done_anim.pos
            self.last_pos = self.rect.center
        if self.anims:
            current_anim = self.anims[0]
            func = self.__class__.toFunc(current_anim.func)
            self.rect.center = func(
                self.last_pos,
                current_anim.pos,
                self.time / current_anim.time
            )
        else:
            self.time = 0

    def addPosAbs(self, func, time, x_or_pair, y=None, sound=None):
        self.anims.append(
            Anim(func, time, x_or_pair, y, sound)
        )

    def addPosRel(self, func, time, x_or_pair, y=None, sound=None):
        newPos = Vec2d(x_or_pair, y)
        if self.anims:
            newPos += self.anims[-1].pos
        else:
            newPos += self.rect.center
        self.addPosAbs(func, time, newPos, sound=sound)

    def addWait(self, time, sound=None):
        self.addPosRel(AnimSprite.Binary, time, 0, 0, sound)
