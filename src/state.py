import jovialengine

from monster import Monster


class State(jovialengine.Saveable):
    __slots__ = (
        'protag_mon',
        'fight_results',
    )

    def __init__(self):
        # start with a random monster
        self.protag_mon = Monster()
        self.fight_results = []

    def save(self):
        return {
            'protag_mon': self.protag_mon,
            'fight_results': self.fight_results,
        }

    @classmethod
    def load(cls, save_data):
        new_obj = cls()
        new_obj.protag_mon = save_data['protag_mon']
        new_obj.fight_results = save_data['fight_results']
        return new_obj
