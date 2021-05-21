import os
import json

import constants
import shared
import saveable
import mode
from state import State


class Save(object):
    __slots__ = (
        'file_name',
        '_mode_name',
        '_mode_data',
        '_shared_data',
    )

    def __init__(self, file_name: str, mode_name: str, mode_data, shared_data):
        self.file_name = file_name
        self._mode_name = mode_name
        self._mode_data = mode_data
        self._shared_data = shared_data

    @staticmethod
    def willOverwrite(file_name: str):
        return os.path.exists(
            os.path.join(constants.SAVE_DIRECTORY, file_name)
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
                os.path.join(constants.SAVE_DIRECTORY, file_name)
            )
        )

    @classmethod
    def getAllFromFiles(cls):
        return tuple(
            sorted(
                (
                    save
                    for save
                    in (
                        cls.getFromFile(file)
                        for file
                        in cls._getSaveFiles()
                    )
                    if save
                ),
                key=lambda s: (s.file_name.lower(), s.file_name)
            )
        )

    @classmethod
    def getFromFile(cls, file_name: str):
        file_path = os.path.join(constants.SAVE_DIRECTORY, file_name)
        try:
            with open(file_path, 'r') as file:
                save_object = json.load(file, object_hook=saveable.decodeSaveable)
                return cls(file_name, save_object['mode_name'], save_object['mode_data'], save_object['shared_data'])
        except (IOError, json.decoder.JSONDecodeError):
            return False

    @classmethod
    def getFromMode(cls, file_name: str, from_mode: saveable.Saveable):
        return cls(file_name, type(from_mode).__name__, from_mode.save(), shared.state.save())

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
        file_path = os.path.join(constants.SAVE_DIRECTORY, self.file_name)
        try:
            with open(file_path, 'w') as file:
                json.dump(save_object, file, cls=saveable.SaveableJSONEncoder)
            return True
        except IOError:
            return False

    def load(self):
        shared.state = State.load(self._shared_data)
        mode_cls = getattr(mode, self._mode_name)
        new_mode = mode_cls.load(self._mode_data)
        return new_mode
