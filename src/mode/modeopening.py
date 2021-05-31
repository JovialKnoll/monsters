import abc

import pygame

from .mode import Mode


class ModeOpening(Mode, abc.ABC):
    @abc.abstractmethod
    def _switchMode(self):
        raise NotImplementedError(
            type(self).__name__ + "._switchMode(self)"
        )

    def _input(self, event):
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self._stopMixer()
            self._switchMode()
