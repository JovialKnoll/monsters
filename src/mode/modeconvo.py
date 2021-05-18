import abc

import pygame

import constants
import utility
import shared
from boxes import Boxes

from .mode import Mode


class ModeConvo(Mode):
    SCROLL_AMOUNT_SPEED = 0.1
    boxes = Boxes(
        (
            pygame.Rect(8, 88, 88, 36),
            pygame.Rect(224, 88, 88, 36),
            pygame.Rect(8, 132, 88, 36),
            pygame.Rect(224, 132, 88, 36),
        ),
        (
            pygame.K_LEFT,
        ),
        (
            pygame.K_RIGHT,
        ),
    )
    black_box = pygame.image.load(constants.BLACKBOX_FILE).convert(shared.display.screen)
    black_box.set_colorkey(constants.COLORKEY)

    __slots__ = (
        'background',
        'text_rect',
        'text_scroll',
        'surf_text',
    )

    def __init__(self):
        super().__init__()

        self.background = pygame.image.load(constants.LAYOUT_1_FILE).convert(shared.display.screen)
        self.background.set_colorkey(constants.COLORKEY)
        # mainly, make the surfaces based on the text for view and buttons, fitting some criteria
        self.text_rect = pygame.Rect(0, 0, 288, 48)
        self.text_scroll = 0
        self.surf_text = shared.font_wrap.renderInside(288, self._textMain(), False, constants.TEXT_COLOR)
        for index, rect in enumerate(type(self).boxes.rects):
            shared.font_wrap.renderToInside(
                self.background,
                self.boxes.textStart(index),
                self.boxes.textWidth(index),
                self._textButton(index),
                False,
                constants.TEXT_COLOR
            )
        # what else do conversations need?

    @abc.abstractmethod
    def _textMain(self):
        # return text for main section
        raise NotImplementedError(type(self).__name__ + "._textMain(self)")

    @abc.abstractmethod
    def _textButton(self, index: int):
        # return text for button
        raise NotImplementedError(type(self).__name__ + "._textButton(self, index)")

    @abc.abstractmethod
    def _goButton(self, index: int):
        # do stuff for button
        raise NotImplementedError(type(self).__name__ + "._goButton(self, index)")

    def _input(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.boxes.posSelect(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.boxes.posSelect(event.pos) is not None \
                    and self._mouseButtonStatus(event.button) \
                    and self.boxes.posSelect(self._mouseButtonStatus(event.button)) \
                        == self.boxes.posSelect(event.pos):
                    self._goButton(self.boxes.select)
            elif event.button == 4:
                self.text_rect.move_ip(0, -constants.FONT_HEIGHT)
            elif event.button == 5:
                self.text_rect.move_ip(0, constants.FONT_HEIGHT)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._goButton(self.boxes.select)
            else:
                self.boxes.keySelect(event.key)

    def update(self, dt):
        self.text_scroll, text_scroll_int = utility.getIntMovement(
            self.text_scroll,
            (pygame.key.get_pressed()[pygame.K_DOWN] - pygame.key.get_pressed()[pygame.K_UP]) * self.SCROLL_AMOUNT_SPEED,
            dt
        )
        self.text_rect.move_ip(0, text_scroll_int)
        self.text_rect.clamp_ip(self.surf_text.get_rect())

    def _drawScreen(self, screen):
        screen.fill(constants.WHITE)
        screen.blit(self.background, (0, 0))
        screen.blit(self.surf_text, (16, 16), self.text_rect)
        screen.blit(self.black_box, self.boxes.getSelectRect())
