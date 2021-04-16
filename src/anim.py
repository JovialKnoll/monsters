from vec2d import Vec2d

class Anim(object):
    __slots__ = (
        'func',
        'time',
        'pos',
        'sound',
    )

    def __getstate__(self):
        return (self.func, self.time, self.pos)

    def __setstate__(self, state):
        self.func, self.time, self.pos = state

    def __init__(self, func, time, x_or_pair, y=None, sound=None):
        self.func = func
        self.time = time
        self.pos = Vec2d(x_or_pair, y)
        self.sound = sound
