from monster import Monster


class State(object):
    __slots__ = (
        'protag_mon',
    )

    def __init__(self):
        self.protag_mon = Monster()

    def save(self):
        # todo: actually return object
        return 1

    @classmethod
    def load(cls, save_data):
        # todo: actually use save_data
        return cls()
