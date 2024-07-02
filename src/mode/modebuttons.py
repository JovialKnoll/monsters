import abc

import pygame
import jovialengine

import constants
from .modescreensize import ModeScreenSize


class ModeButtons(ModeScreenSize, abc.ABC):
    _TEXT_MARGIN = 4
    buttons = ()

    __slots__ = (
        '_black_box',
        '_selected_button',
        '_clicked_button',
    )

    def __init__(self):
        super().__init__()
        self._black_box = jovialengine.load.image(constants.BLACKBOX_FILE, constants.COLORKEY)
        self._selected_button = 0
        self._clicked_button = None

    def _draw_selected(self, screen: pygame.surface):
        screen.blit(self._black_box, self.buttons[self._selected_button])

    def _key_select(self, change: int):
        self._selected_button += change
        self._selected_button %= len(self.buttons)

    def _pos_select_button(self, pos: tuple[int, int], index: int, rect: pygame.rect):
        if rect.collidepoint(pos):
            self._selected_button = index
            return self._selected_button
        return None

    def _pos_select(self, pos: tuple[int, int]):
        for index, rect in enumerate(self.buttons):
            selected_button = self._pos_select_button(pos, index, rect)
            if selected_button is not None:
                return selected_button
        return None

    @classmethod
    def _text_start(cls, index: int):
        return (
            cls.buttons[index].x + cls._TEXT_MARGIN,
            cls.buttons[index].y + cls._TEXT_MARGIN,
        )

    @classmethod
    def _text_width(cls, index: int):
        return cls.buttons[index].w - (cls._TEXT_MARGIN * 2)

    @abc.abstractmethod
    def _button_press(self):
        raise NotImplementedError(
            type(self).__name__ + "._buttonPress(self)"
        )

    def _take_event(self, event):
        # using this for button selection and pressing
        if event.type == pygame.MOUSEMOTION:
            self._pos_select(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._pos_select(event.pos)
                self._clicked_button = self._selected_button
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self._pos_select(event.pos) is not None \
                        and self._selected_button == self._clicked_button:
                    self._button_press()
                self._clicked_button = None

    def _take_frame(self, input_frame):
        if input_frame.was_input_pressed(constants.EVENT_CONFIRM):
            self._button_press()
        if input_frame.was_input_pressed(constants.EVENT_LEFT):
            self._key_select(-1)
        if input_frame.was_input_pressed(constants.EVENT_RIGHT):
            self._key_select(1)
