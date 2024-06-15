import abc

import pygame

import constants
from .modescreensize import ModeScreenSize


class ModeOpening(ModeScreenSize, abc.ABC):
    @abc.abstractmethod
    def _switchMode(self):
        raise NotImplementedError(
            type(self).__name__ + "._switchMode(self)"
        )

    def _inputEvent(self, event):
        if event.type == pygame.KEYDOWN \
            or (
                event.type == pygame.MOUSEBUTTONUP
                and event.button == 1
                ):
            self._stopMixer()
            self._switchMode()

    def _inputFrame(self, input_frame):
        if input_frame.wasAnyInputPressed(constants.ALL_EVENTS):
            self._stopMixer()
            self._switchMode()
