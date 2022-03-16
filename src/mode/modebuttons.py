import abc

import pygame
import jovialengine

import constants


class ModeButtons(jovialengine.ModeBase, abc.ABC):
    _TEXT_MARGIN = 4
    buttons = ()
    _back_keys = set()
    _forward_keys = set()

    __slots__ = (
        '_black_box',
        '_selected_button',
    )

    def __init__(self):
        super().__init__()
        self._black_box = pygame.image.load(constants.BLACKBOX_FILE).convert(self._space)
        self._black_box.set_colorkey(constants.COLORKEY)
        self._selected_button = 0

    def _drawSelected(self, screen: pygame.surface):
        screen.blit(self._black_box, self.buttons[self._selected_button])

    def _keySelect(self, key):
        if key in self._back_keys:
            self._selected_button -= 1
        elif key in self._forward_keys:
            self._selected_button += 1
        self._selected_button %= len(self.buttons)

    def _posSelectButton(self, pos: tuple[int, int], index: int, rect: pygame.rect):
        if rect.collidepoint(pos):
            self._selected_button = index
            return self._selected_button
        return None

    def _posSelect(self, pos: tuple[int, int]):
        for index, rect in enumerate(self.buttons):
            selected_button = self._posSelectButton(pos, index, rect)
            if selected_button is not None:
                return selected_button
        return None

    @classmethod
    def _textStart(cls, index: int):
        return (
            cls.buttons[index].x + cls._TEXT_MARGIN,
            cls.buttons[index].y + cls._TEXT_MARGIN,
        )

    @classmethod
    def _textWidth(cls, index: int):
        return cls.buttons[index].w - (cls._TEXT_MARGIN * 2)

    @abc.abstractmethod
    def _buttonPress(self):
        raise NotImplementedError(
            type(self).__name__ + "._buttonPress(self)"
        )

    def _input(self, event):
        # using this for button selection and pressing
        if event.type == pygame.MOUSEMOTION:
            self._posSelect(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._posSelect(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self._posSelect(event.pos) is not None \
                    and self._mouseButtonStatus(event.button) \
                    and self._posSelect(self._mouseButtonStatus(event.button)) \
                        == self._posSelect(event.pos):
                    self._buttonPress()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._buttonPress()
            else:
                self._keySelect(event.key)
