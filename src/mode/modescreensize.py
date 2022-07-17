import abc

import jovialengine

import constants


class ModeScreenSize(jovialengine.ModeBase, abc.ABC):
    def __init__(self):
        self._init(constants.SCREEN_SIZE)
