import pygame
import jovialengine

import constants


class Star(jovialengine.AnimSprite):
    _IMAGE_LOCATION = constants.STAR
    _ALPHA_OR_COLORKEY = constants.COLORKEY

    def __init__(self, pos: pygame.typing.Point = (0, 0)):
        print(f"Star {pos}")
        print(self._IMAGE_LOCATION)
        print(self._ALPHA_OR_COLORKEY)
        super().__init__(pos)
