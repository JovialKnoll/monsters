import abc

import pygame

import constants
from .modescreensize import ModeScreenSize


class ModeOpening(ModeScreenSize, abc.ABC):
    @abc.abstractmethod
    def _switch_mode(self):
        raise NotImplementedError(
            type(self).__name__ + "._switch_mode(self)"
        )

    def _take_event(self, event):
        if event.type == pygame.KEYDOWN \
            or (
                event.type == pygame.MOUSEBUTTONUP
                and event.button == 1
                ):
            self._stop_mixer()
            self._switch_mode()

    def _take_frame(self, input_frame):
        if input_frame.was_any_input_pressed(constants.ALL_EVENTS):
            self._stop_mixer()
            self._switch_mode()
