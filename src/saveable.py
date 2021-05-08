import sys
import abc
import json
from collections import deque


class Saveable(abc.ABC):
    @abc.abstractmethod
    def save(self):
        """Return an object represented all the information that should be saved from this mode."""
        raise NotImplementedError(
            type(self).__name__ + ".saveMode(self)"
        )

    @classmethod
    @abc.abstractmethod
    def load(cls, save_data):
        """Take in an object equivalent to the result of a call to saveMode(), and return an instance of this mode."""
        raise NotImplementedError(
            cls.__name__ + ".loadMode(cls, saveData)"
        )


class SaveableJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, deque):
            return {
                'COLLECTION': 'DEQUE',
                'ELEMENTS': list(o),
                'MAXLEN': o.maxlen,
            }
        elif isinstance(o, type):
            return {
                'MODULE': o.__module__,
                'CLASS': o.__qualname__,
            }
        elif isinstance(o, Saveable):
            return {
                'MODULE': type(o).__module__,
                'CLASS': type(o).__qualname__,
                'SAVEABLE': o.save(),
            }
        return super().default(o)


def _getClass(dct: dict):
    attr = sys.modules[dct['MODULE']]
    for name in dct['CLASS'].split('.'):
        attr = getattr(attr, name)
    return attr


def decodeSaveable(dct: dict):
    if 'COLLECTION' in dct:
        if dct['COLLECTION'] == 'DEQUE':
            return deque(dct['ELEMENTS'], dct['MAXLEN'])
    elif {'MODULE', 'CLASS'} == dct.keys():
        return _getClass(dct)
    elif {'MODULE', 'CLASS', 'SAVEABLE'} == dct.keys():
        saveable_class = _getClass(dct)
        return saveable_class.load(dct['SAVEABLE'])
    return dct
