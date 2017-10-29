from collections import deque

import pygame

from anim import Anim

class AnimSprite(pygame.sprite.Sprite):
    class Type(object):
        Lerp, IncSpeed, DecSpeed, IncDecSpeed, DecIncSpeed = range(5)
    __slots__ = (
        'anims',
        'last_pos',
    )
    def __getstate__(self):
        return (self.rect, self.anims)
    def __setstate__(self, state):
        super(AnimSprite, self).__init__()
        self.rect, self.anims = state

    def __init__(self):
        super(AnimSprite, self).__init__()
        self.anims = deque()

    def update(self, *args):
        if not anims:
            return
        dt = args[0]
        

    def addAnimAbs(self, type, time, x_or_pair, y = None):
        anims.appendleft(
            Anim(type, time, x_or_pair, y)
        )

    def addAnimRel(self, type, time, x_or_pair, y = None):
        newPos = Vec2d(x_or_pair, y)
        if anims:
            newPos += anims[0].vec
        else:
            newPos += self.rect.topleft
        self.addAnimAbs(type, time, newPos)
