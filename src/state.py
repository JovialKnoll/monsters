from monster import *

class State(object):
    __slots__ = (
        'protag_mon',
    )

    def __init__(self):
        self.protag_mon = Monster()

state = State()
