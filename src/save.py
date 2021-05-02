import os

import pygame

import constants
import shared
import mode
from state import State

class Save(object):
    __slots__ = (
        'file_name',
        '_mode_name',
        '_mode_data',
        '_shared_data',
    )

    def __init__(self, file_name, mode_name, mode_data, shared_data):
        self.file_name = file_name
        self._mode_name = mode_name
        self._mode_data = mode_data
        self._shared_data = shared_data

    @classmethod
    def getFromMode(cls, file_name, from_mode: mode.Mode):
        return cls(file_name, type(from_mode).__name__, from_mode.save(), shared.state.save())

    @classmethod
    def getFromFile(cls, file_name):
        try:
            # todo: actually implement opening and parsing file
            return cls(file_name, "ModeTest", 1, "REPLACE WITH SHARED DATA")
            pass
        except IOError:
            return False

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
                key=lambda s: s.file_name
            )
        )

    @classmethod
    def willOverwrite(cls, file_name):
        for f in cls._getSaveFiles():
            print(f)
        print(file_name)
        return file_name in cls._getSaveFiles()

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

    def save(self):
        try:
            os.mkdir(constants.SAVE_DIRECTORY)
        except FileExistsError:
            pass
        try:
            file_path = os.path.join(constants.SAVE_DIRECTORY, self.file_name)
            with open(file_path, 'w') as file:
                # todo: actually write out information
                print("REPLACE WITH ACTUAL WRITING TO FILE", file=file)
            return True
        except IOError:
            return False
        # objects = ['asd', (1, 2, 3), 123]
        # if not os.path.exists(constants.SAVE_DIRECTORY):
        #     os.makedirs(constants.SAVE_DIRECTORY)
        # with open(
        #         os.path.join(
        #             constants.SAVE_DIRECTORY,
        #             self._save_name + self.file_extension
        #         ),
        #         'wb'
        # ) as f:
        #    pickle.dump(objects, f, pickle.HIGHEST_PROTOCOL)

    def load(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.stop()
        shared.state = State.load(self._shared_data)
        mode_cls = getattr(mode, self._mode_name)
        new_mode = mode_cls.load(self._mode_data)
        pygame.mixer.music.pause()
        pygame.mixer.pause()
        return new_mode
