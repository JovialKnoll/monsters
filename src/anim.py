from vec2d import Vec2d

class Anim(object):
    __slots__ = (
        'type',
        'time',
        'pos',
    )
    def __getstate__(self):
        return (self.type, self.time, self.pos)
    def __setstate__(self, state):
        self.type, self.time, self.pos = state

    def __init__(self, type, time, x_or_pair, y = None):
        self.type = type
        self.time = time
        self.pos = Vec2d(x_or_pair, y)
