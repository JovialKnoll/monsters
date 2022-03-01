from collections import deque

import pygame

import constants
import utility
from saveable import Saveable


class Anim(Saveable):
    __slots__ = (
        'func',
        'time',
        'pos',
        'sound',
        'positional_sound',
    )

    def __init__(self, func: str, time: int, x_or_pair, y=None,
                 sound: pygame.mixer.Sound = None, positional_sound: bool = False):
        self.func = func
        self.time = time
        self.pos = pygame.math.Vector2(x_or_pair, y)
        self.sound = sound
        self.positional_sound = positional_sound

    def save(self):
        # no sound right now, sorry
        # if we need it, either start passing sounds as paths
        # or don't save when there are pending Anims
        return self.func, self.time, self.pos

    @classmethod
    def load(cls, save_data):
        return cls(*save_data)


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
        'positional_sound',
        'sound_channel',
    )

    def __init__(self):
        super().__init__()
        # dirty = 2 : always draw
        self.dirty = 2
        self.anims = deque()
        self.last_pos = None
        self.time = 0
        self.positional_sound = False
        self.sound_channel = None

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
            self.time -= done_anim.time
            self.rect.center = done_anim.pos
            self.last_pos = self.rect.center
            if done_anim.sound:
                self.positional_sound = done_anim.positional_sound
                channel = done_anim.sound.play()
                if self.positional_sound:
                    self.sound_channel = channel
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
        if self.positional_sound:
            if self.sound_channel.get_busy():
                pos = min(max(self.rect.centerx / constants.SCREEN_SIZE[0], 0), 1)
                channel_l = self._boundChannelVolume(utility.cos_curve(pos))
                channel_r = self._boundChannelVolume(utility.sin_curve(pos))
                self.sound_channel.set_volume(channel_l, channel_r)
            else:
                self.positional_sound = False
                self.sound_channel = None

    @staticmethod
    def _boundChannelVolume(volume):
        return .2 + (volume * .8)

    def addPosAbs(self, func, time, x_or_pair, y=None, sound=None, positional_sound=False):
        self.anims.append(
            Anim(func, time, x_or_pair, y, sound, positional_sound)
        )

    def addPosRel(self, func, time, x_or_pair, y=None, sound=None, positional_sound=False):
        new_pos = pygame.math.Vector2(x_or_pair, y)
        if self.anims:
            new_pos += self.anims[-1].pos
        else:
            new_pos += self.rect.center
        self.addPosAbs(func, time, new_pos, sound=sound, positional_sound=positional_sound)

    def addWait(self, time, sound=None, positional_sound=False):
        self.addPosRel(AnimSprite.Binary, time, 0, 0, sound, positional_sound)
