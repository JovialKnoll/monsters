import os

import constants
import shared


def saveGame(fileName, game_mode):
    # write out game_mode details and shared details to file
    # use a try, return false if fails
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


def loadGame(save):
    # update shared state
    # create game mode and return it
    pass


def willSaveOverwrite(fileName):
    return fileName in _getSaveFiles()


def getSaves():
    if os.path.isdir(constants.SAVE_DIRECTORY):
        return tuple(
            save
            for save
            in (
                _getSave(file)
                for file
                in _getSaveFiles()
            )
            if save
        )
    return ()


def _getSaveFiles():
    return (
        file
        for file
        in os.listdir(constants.SAVE_DIRECTORY)
        if os.path.isfile(file)
    )


def _getSave(file):
    # return save object from save file
    return False
