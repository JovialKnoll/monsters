import abc

import pygame

import constants
import shared

from .mode import Mode


class ModeButtons(Mode, abc.ABC):
    _TEXT_MARGIN = 4
    _black_box = pygame.image.load(constants.BLACKBOX_FILE).convert(shared.display.screen)
    _black_box.set_colorkey(constants.COLORKEY)
    buttons = ()
    _back_keys = set()
    _forward_keys = set()

    __slots__ = (
        '_selected_button',
    )

    def __init__(self):
        super().__init__()
        self._selected_button = 0

    def drawSelected(self, screen):
        screen.blit(self._black_box, self.buttons[self._selected_button])

    def keySelect(self, key):
        if key in self._back_keys:
            self._selected_button -= 1
        elif key in self._forward_keys:
            self._selected_button += 1
        self._selected_button %= len(self.buttons)

    def posSelect(self, pos: tuple[int], selectable_buttons=None):
        # replace selectable_buttons nonsense with overridden function
        for index, rect in enumerate(self.buttons):
            if selectable_buttons and index >= selectable_buttons:
                return None
            elif rect.collidepoint(pos):
                self._selected_button = index
                return self._selected_button
        return None

    @classmethod
    def textStart(cls, index: int):
        return (
            cls.buttons[index].x + cls._TEXT_MARGIN,
            cls.buttons[index].y + cls._TEXT_MARGIN,
        )

    @classmethod
    def textWidth(cls, index: int):
        return cls.buttons[index].w - (cls._TEXT_MARGIN * 2)

    # def _input(self, event):
    #     if event.type == pygame.MOUSEMOTION:
    #         self.boxes.posSelect(event.pos, len(self._buttons))
    #     elif event.type == pygame.MOUSEBUTTONUP:
    #         if event.button == 1:
    #             if self._read_text \
    #                 and self.boxes.posSelect(event.pos, len(self._buttons)) is not None \
    #                 and self._mouseButtonStatus(event.button) \
    #                 and self.boxes.posSelect(self._mouseButtonStatus(event.button), len(self._buttons)) \
    #                     == self.boxes.posSelect(event.pos, len(self._buttons)):
    #                 self._selectButton(self.boxes.select)
    #         elif event.button == 4:
    #             self._text_rect.move_ip(0, -constants.FONT_HEIGHT)
    #         elif event.button == 5:
    #             self._text_rect.move_ip(0, constants.FONT_HEIGHT)
    #     elif event.type == pygame.KEYDOWN and self._read_text:
    #         if event.key == pygame.K_RETURN:
    #             self._selectButton(self.boxes.select)
    #         else:
    #             self.boxes.keySelect(event.key, len(self._buttons))
    #
    # def _update(self, dt):
    #     pressed_keys = pygame.key.get_pressed()
    #     self._text_scroll, text_scroll_int = utility.getIntMovement(
    #         self._text_scroll,
    #         (pressed_keys[pygame.K_DOWN] - pressed_keys[pygame.K_UP]) * self.SCROLL_AMOUNT_SPEED,
    #         dt
    #     )
    #     self._text_rect.move_ip(0, text_scroll_int)
    #     self._text_rect.clamp_ip(self._surf_text.get_rect())
    #     if self._text_rect.bottom >= self._surf_text.get_rect().bottom:
    #         self._read_text = True
