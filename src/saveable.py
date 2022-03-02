import sys
import abc
import json
from collections import deque

import pygame.math


class Saveable(abc.ABC):
    @abc.abstractmethod
    def save(self):
        """Return a serializable object representing all the information that should be saved from this object."""
        raise NotImplementedError(
            type(self).__name__ + ".saveMode(self)"
        )

    @classmethod
    @abc.abstractmethod
    def load(cls, save_data):
        """Take in an object (the result of a call to save()), and return an instance of this object."""
        raise NotImplementedError(
            cls.__name__ + ".loadMode(cls, saveData)"
        )


_KEY_COLLECTION = 'COLLECTION'
_COLLECTION_DEQUE = 'DEQUE'
_COLLECTION_SET = 'SET'
_COLLECTION_VECTOR2 = 'VECTOR2'
_COLLECTION_VECTOR3 = 'VECTOR3'
_KEY_ELEMENTS = 'ELEMENTS'
_KEY_MAXLEN = 'MAXLEN'
_KEY_MODULE = 'MODULE'
_KEY_CLASS = 'CLASS'
_KEY_SAVEABLE = 'SAVEABLE'


class SaveableJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, deque):
            return {
                _KEY_COLLECTION: _COLLECTION_DEQUE,
                _KEY_ELEMENTS: list(o),
                _KEY_MAXLEN: o.maxlen,
            }
        elif isinstance(o, set):
            return {
                _KEY_COLLECTION: _COLLECTION_SET,
                _KEY_ELEMENTS: list(o),
            }
        elif isinstance(o, pygame.math.Vector2):
            return {
                _KEY_COLLECTION: _COLLECTION_VECTOR2,
                _KEY_ELEMENTS: list(o),
            }
        elif isinstance(o, pygame.math.Vector3):
            return {
                _KEY_COLLECTION: _COLLECTION_VECTOR3,
                _KEY_ELEMENTS: list(o),
            }
        elif isinstance(o, type):
            return {
                _KEY_MODULE: o.__module__,
                _KEY_CLASS: o.__qualname__,
            }
        elif isinstance(o, Saveable):
            return {
                _KEY_MODULE: type(o).__module__,
                _KEY_CLASS: type(o).__qualname__,
                _KEY_SAVEABLE: o.save(),
            }
        return super().default(o)


def _getClass(dct: dict):
    attr = sys.modules[dct[_KEY_MODULE]]
    for name in dct[_KEY_CLASS].split('.'):
        attr = getattr(attr, name)
    return attr


def decodeSaveable(dct: dict):
    if _KEY_COLLECTION in dct:
        if dct[_KEY_COLLECTION] == _COLLECTION_DEQUE:
            return deque(dct[_KEY_ELEMENTS], dct[_KEY_MAXLEN])
        elif dct[_KEY_COLLECTION] == _COLLECTION_SET:
            return set(dct[_KEY_ELEMENTS])
        elif dct[_KEY_COLLECTION] == _COLLECTION_VECTOR2:
            return pygame.math.Vector2(dct[_KEY_ELEMENTS])
        elif dct[_KEY_COLLECTION] == _COLLECTION_VECTOR3:
            return pygame.math.Vector3(dct[_KEY_ELEMENTS])
    elif {_KEY_MODULE, _KEY_CLASS} == dct.keys():
        return _getClass(dct)
    elif {_KEY_MODULE, _KEY_CLASS, _KEY_SAVEABLE} == dct.keys():
        saveable_class = _getClass(dct)
        return saveable_class.load(dct[_KEY_SAVEABLE])
    return dct
