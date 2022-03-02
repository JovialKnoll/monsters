import sys
import os
import json
from collections import deque

import pygame.math

import constants
import shared
import mode
from saveable import Saveable
from state import State


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


class _SaveableJSONEncoder(json.JSONEncoder):
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


def _decodeSaveable(dct: dict):
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


_SAVE_EXT = '.sav'


class Save(object):
    __slots__ = (
        'save_name',
        '_mode_name',
        '_mode_data',
        '_shared_data',
    )

    def __init__(self, save_name: str, mode_name: str, mode_data, shared_data):
        self.save_name = save_name
        self._mode_name = mode_name
        self._mode_data = mode_data
        self._shared_data = shared_data

    @staticmethod
    def willOverwrite(save_name: str):
        return os.path.exists(
            Save._getFilePathFromFileName(save_name + _SAVE_EXT)
        )

    @staticmethod
    def _getSaveFiles():
        if not os.path.isdir(constants.SAVE_DIRECTORY):
            return ()
        return (
            file_name
            for file_name
            in os.listdir(constants.SAVE_DIRECTORY)
            if os.path.isfile(
                Save._getFilePathFromFileName(file_name)
            )
            and file_name.endswith(_SAVE_EXT)
        )

    @staticmethod
    def _getFilePathFromFileName(file_name):
        return os.path.join(constants.SAVE_DIRECTORY, file_name)

    def _getFilePath(self):
        return self._getFilePathFromFileName(self.save_name + _SAVE_EXT)

    @classmethod
    def getAllFromFiles(cls):
        return sorted(
            (
                save
                for save
                in (
                    cls._getFromFile(file)
                    for file
                    in cls._getSaveFiles()
                )
                if save
            ),
            key=lambda s: (s.save_name.lower(), s.save_name)
        )

    @classmethod
    def _getFromFile(cls, file_name: str):
        file_path = cls._getFilePathFromFileName(file_name)
        try:
            with open(file_path, 'r') as file:
                save_object = json.load(file, object_hook=_decodeSaveable)
                return cls(file_name[:-len(_SAVE_EXT)], save_object['mode_name'], save_object['mode_data'], save_object['shared_data'])
        except (IOError, json.decoder.JSONDecodeError):
            return False

    @classmethod
    def getFromMode(cls, save_name: str, from_mode: Saveable):
        return cls(save_name, type(from_mode).__name__, from_mode.save(), shared.state.save())

    def save(self):
        try:
            os.mkdir(constants.SAVE_DIRECTORY)
        except FileExistsError:
            pass
        save_object = {
            'mode_name': self._mode_name,
            'mode_data': self._mode_data,
            'shared_data': self._shared_data,
        }
        file_path = self._getFilePath()
        try:
            with open(file_path, 'w') as file:
                json.dump(save_object, file, cls=_SaveableJSONEncoder)
            return True
        except IOError:
            return False

    def load(self):
        shared.state = State.load(self._shared_data)
        mode_cls = getattr(mode, self._mode_name)
        new_mode = mode_cls.load(self._mode_data)
        return new_mode

    def delete(self):
        file_path = self._getFilePath()
        os.remove(file_path)
