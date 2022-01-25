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


KEY_COLLECTION = 'COLLECTION'
COLLECTION_DEQUE = 'DEQUE'
COLLECTION_SET = 'SET'
COLLECTION_VECTOR2 = 'VECTOR2'
COLLECTION_VECTOR3 = 'VECTOR3'
KEY_ELEMENTS = 'ELEMENTS'
KEY_MAXLEN = 'MAXLEN'
KEY_MODULE = 'MODULE'
KEY_CLASS = 'CLASS'
KEY_SAVEABLE = 'SAVEABLE'


class SaveableJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, deque):
            return {
                KEY_COLLECTION: COLLECTION_DEQUE,
                KEY_ELEMENTS: list(o),
                KEY_MAXLEN: o.maxlen,
            }
        elif isinstance(o, set):
            return {
                KEY_COLLECTION: COLLECTION_SET,
                KEY_ELEMENTS: list(o),
            }
        elif isinstance(o, pygame.math.Vector2):
            return {
                KEY_COLLECTION: COLLECTION_VECTOR2,
                KEY_ELEMENTS: list(o),
            }
        elif isinstance(o, pygame.math.Vector3):
            return {
                KEY_COLLECTION: COLLECTION_VECTOR3,
                KEY_ELEMENTS: list(o),
            }
        elif isinstance(o, type):
            return {
                KEY_MODULE: o.__module__,
                KEY_CLASS: o.__qualname__,
            }
        elif isinstance(o, Saveable):
            return {
                KEY_MODULE: type(o).__module__,
                KEY_CLASS: type(o).__qualname__,
                KEY_SAVEABLE: o.save(),
            }
        return super().default(o)


def _getClass(dct: dict):
    attr = sys.modules[dct[KEY_MODULE]]
    for name in dct[KEY_CLASS].split('.'):
        attr = getattr(attr, name)
    return attr


def decodeSaveable(dct: dict):
    if KEY_COLLECTION in dct:
        if dct[KEY_COLLECTION] == COLLECTION_DEQUE:
            return deque(dct[KEY_ELEMENTS], dct[KEY_MAXLEN])
        elif dct[KEY_COLLECTION] == COLLECTION_SET:
            return set(dct[KEY_ELEMENTS])
        elif dct[KEY_COLLECTION] == COLLECTION_VECTOR2:
            return pygame.math.Vector2(dct[KEY_ELEMENTS])
        elif dct[KEY_COLLECTION] == COLLECTION_VECTOR3:
            return pygame.math.Vector3(dct[KEY_ELEMENTS])
    elif {KEY_MODULE, KEY_CLASS} == dct.keys():
        return _getClass(dct)
    elif {KEY_MODULE, KEY_CLASS, KEY_SAVEABLE} == dct.keys():
        saveable_class = _getClass(dct)
        return saveable_class.load(dct[KEY_SAVEABLE])
    return dct
