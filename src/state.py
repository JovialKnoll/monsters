from monster import Monster


class State(object):
    __slots__ = (
        'protag_mon',
    )

    def __init__(self):
        self.protag_mon = Monster()

    def save(self):
        return {
            'protag_mon': self.protag_mon.save()
        }

    @classmethod
    def load(cls, save_data):
        new_state = cls()
        new_state.protag_mon = Monster.load(save_data['protag_mon'])
        return new_state
