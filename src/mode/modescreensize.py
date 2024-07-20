import abc

import jovialengine

import constants


class ModeScreenSize(jovialengine.ModeBase, abc.ABC):
    _SPACE_SIZE = constants.SCREEN_SIZE
