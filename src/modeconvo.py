import pygame

import constants
import utility
import shared
from mode import Mode
from boxes import Boxes

class ModeConvo(Mode):
    scroll_amount_speed = 0.1
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
        super(ModeConvo, self).__init__()

        self.background = pygame.image.load(constants.LAYOUT_1_FILE).convert(shared.display.screen)
        self.background.set_colorkey(constants.COLORKEY)
        # mainly, make the surfaces based on the text for view and buttons, fitting some criteria
        self.text_rect = pygame.Rect(0, 0, 288, 48)
        self.text_scroll = 0
        self.surf_text = shared.font_wrap.renderInside(288, self._textMain(), False, constants.TEXT_COLOR)
        for index, rect in enumerate(self.__class__.boxes.rects):
            shared.font_wrap.renderToInside(
                self.background,
                self.__class__.boxes.textStart(index),
                self.__class__.boxes.textWidth(index),
                self._textButton(index),
                False,
                constants.TEXT_COLOR
            )
        # what else do conversations need?

    def _textMain(self):
        # return text for main section
        raise NotImplementedError(self.__class__.__name__ + "._textMain(self)")
    def _textButton(self, index):
        # return text for button
        raise NotImplementedError(self.__class__.__name__ + "._textButton(self, index)")
    def _goButton(self, index):
        # do stuff for button
        raise NotImplementedError(self.__class__.__name__ + "._goButton(self, index)")

    def _input(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.__class__.boxes.posSelect(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.__class__.boxes.posSelect(event.pos) is not None:
                    self._goButton(self.__class__.boxes.select)
            elif event.button == 4:
                self.text_rect.move_ip(0, -constants.FONT_HEIGHT)
            elif event.button == 5:
                self.text_rect.move_ip(0, constants.FONT_HEIGHT)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._goButton(self.__class__.boxes.select)
            else:
                self.__class__.boxes.keySelect(event.key)

    def update(self, dt):
        self.text_scroll, text_scroll_int = utility.getIntMovement(
            self.text_scroll,
            (self._keyStatus(pygame.K_DOWN) - self._keyStatus(pygame.K_UP)) * self.__class__.scroll_amount_speed,
            dt
        )
        self.text_rect.move_ip(0, text_scroll_int)
        self.text_rect.clamp_ip(self.surf_text.get_rect())

    def _drawScreen(self, screen):
        screen.fill(constants.WHITE)
        screen.blit(self.background, (0, 0))
        screen.blit(self.surf_text, (16, 16), self.text_rect)
        screen.blit(self.__class__.black_box, self.__class__.boxes.getSelectRect())
