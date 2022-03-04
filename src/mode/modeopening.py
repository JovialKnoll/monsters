import abc

import pygame

from jovialengine import ModeBase


class ModeOpening(Mode, abc.ABC):
    @abc.abstractmethod
    def _switchMode(self):
        raise NotImplementedError(
            type(self).__name__ + "._switchMode(self)"
        )

    def _input(self, event):
        if event.type == pygame.KEYDOWN \
            or (
                event.type == pygame.MOUSEBUTTONUP
                and event.button == 1
                ):
            self._stopMixer()
            self._switchMode()
