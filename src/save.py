import os

import constants
import shared


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
    def fromMode(cls, file_name, mode):
        # return Save object based on current shared and mode passed in
        # cls.(file_name, ETC, mode.saveMode, ETC)
        return False

    @classmethod
    def fromFile(cls, file_name):
        # try to open and parse file
        # return Save object, otherwise return False
        # cls.(file_name, parse out the rest)
        return False

    def save(self):
        # write out information to file
        # use a try, return False if fails
        # otherwise return True
        pass
        # objects = ['asd', (1, 2, 3), 123]
        # if not os.path.exists(constants.SAVE_DIRECTORY):
        #     os.makedirs(constants.SAVE_DIRECTORY)
        # with open(
        #         os.path.join(
        #             constants.SAVE_DIRECTORY,
        #             self._save_name + self.__class__.file_extension
        #         ),
        #         'wb'
        # ) as f:
        #    pickle.dump(objects, f, pickle.HIGHEST_PROTOCOL)

    def load(self):
        # update shared state based on self.shared_data
        # instantiate mode: call out to mode.loadMode(self.mode_data)
        # choose the right mode based on self.mode_name
        # return new mode
        pass


def willSaveOverwrite(file_name):
    return file_name in _getSaveFiles()


def getSaves():
    return tuple(
        sorted(
            save
            for save
            in (
                Save.fromFile(file)
                for file
                in _getSaveFiles()
            )
            if save
        )
    )


def _getSaveFiles():
    if not os.path.isdir(constants.SAVE_DIRECTORY):
        return ()
    return (
        file
        for file
        in os.listdir(constants.SAVE_DIRECTORY)
        if os.path.isfile(file)
    )
