import pygame.math
import pygame.mixer

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
