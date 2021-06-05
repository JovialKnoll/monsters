from collections import deque

import pygame

import constants
import utility
from anim import Anim
from vec2d import Vec2d
from saveable import Saveable


class AnimSprite(pygame.sprite.DirtySprite, Saveable):
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

    def __init__(self):
        super().__init__()
        # dirty = 2 : always draw
        self.dirty = 2
        self.anims = deque()
        self.last_pos = None
        self.time = 0

    def save(self):
        return {
            'rect_topleft': self.rect.topleft,
            'anims': self.anims,
            'last_pos': self.last_pos,
            'time': self.time,
        }

    @classmethod
    def load(cls, save_data):
        new_obj = cls()
        new_obj.rect.topleft = save_data['rect_topleft']
        new_obj.anims = save_data['anims']
        new_obj.last_pos = save_data['last_pos']
        new_obj.time = save_data['time']
        return new_obj

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
            if done_anim.sound:
                done_anim.sound.play()
            self.time -= done_anim.time
            self.rect.center = done_anim.pos
            self.last_pos = self.rect.center
        if self.anims:
            current_anim = self.anims[0]
            func = self.toFunc(current_anim.func)
            self.rect.center = func(
                self.last_pos,
                current_anim.pos,
                self.time / current_anim.time
            )
        else:
            self.last_pos = None
            self.time = 0
        # take care of positional audio here
        pos = min(max(self.rect.centerx / constants.SCREEN_SIZE[0], 0), 1)
        channel_l = .75 - (pos * .5)
        channel_r = .25 + (pos * .5)

    def addPosAbs(self, func, time, x_or_pair, y=None, sound=None, positional_sound=False):
        self.anims.append(
            Anim(func, time, x_or_pair, y, sound, positional_sound)
        )

    def addPosRel(self, func, time, x_or_pair, y=None, sound=None, positional_sound=False):
        newPos = Vec2d(x_or_pair, y)
        if self.anims:
            newPos += self.anims[-1].pos
        else:
            newPos += self.rect.center
        self.addPosAbs(func, time, newPos, sound=sound, positional_sound=positional_sound)

    def addWait(self, time, sound=None, positional_sound=False):
        self.addPosRel(AnimSprite.Binary, time, 0, 0, sound, positional_sound)
