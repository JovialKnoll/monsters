import os
import copy

import pygame

import constants
import utility
import shared
from convopart import ConvoPart

from saveable import Saveable
from .modebuttons import ModeButtons


class ModeConvo(ModeButtons, Saveable):
    buttons = (
        pygame.Rect(8, 88, 88, 36),
        pygame.Rect(224, 88, 88, 36),
        pygame.Rect(8, 132, 88, 36),
        pygame.Rect(224, 132, 88, 36),
    )
    _back_keys = {
        pygame.K_LEFT,
        pygame.K_a,
    }
    _forward_keys = {
        pygame.K_RIGHT,
        pygame.K_d,
    }
    SCROLL_AMOUNT_SPEED = 0.1

    __slots__ = (
        '_convo_key',
        '_convo_dict',
        '_style',
        '_text',
        '_choices',
        '_read_text',
        '_text_rect',
        '_text_scroll',
        '_surf_text',
        '_background',
    )

    def keySelect(self, key):
        super().keySelect(key)
        self._selected_button %= len(self._choices)

    def __init__(self, convo_key: str = '0'):
        super().__init__()
        self._convo_key = convo_key
        self._convo_dict = self._getScript()
        self._loadText()
        self._resetPosition()
        self._renderText()

    @classmethod
    def _getScript(cls):
        convo_file = os.path.join(
            constants.CONVO_DIRECTORY,
            cls.__name__.lower() + ".csv"
        )
        return ConvoPart.getConvoDict(convo_file)

    def save(self):
        return self._convo_key

    @classmethod
    def load(cls, save_data):
        new_obj = cls(save_data)
        return new_obj

    def _handleLoad(self):
        """This function will handle any special case logic for loading.
        This is called after loading in the next (or initial) convo part but before rendering it.
        This is called before any button specific logic.
        """
        pass

    def _getTextReplace(self):
        return {
            'MONSTER_NAME': shared.state.protag_mon.name,
        }

    def _loadText(self):
        convo_part = self._convo_dict[self._convo_key]
        # copy so that alterations don't affect basis
        self._style = copy.copy(convo_part.style)
        self._text = convo_part.text.format(**self._getTextReplace())
        self._choices = copy.copy(convo_part.choices)
        self._handleLoad()

    def _resetPosition(self):
        self._read_text = False
        self._text_rect = pygame.Rect(0, 0, 296, 56)
        self._text_scroll = 0
        self._selected_button = 0

    def _renderText(self):
        self._handleTags()
        self._surf_text = shared.font_wrap.renderInside(296, self._text, False, constants.TEXT_COLOR)
        self._background = pygame.image.load(constants.LAYOUT_1_FILE).convert(shared.display.screen)
        self._background.set_colorkey(constants.COLORKEY)
        for index, button in enumerate(self._choices):
            shared.font_wrap.renderToInside(
                self._background,
                self.textStart(index),
                self.textWidth(index),
                button.text,
                False,
                constants.TEXT_COLOR
            )
        for index in range(len(self._choices), 4):
            self._background.fill(constants.WHITE, self.buttons[index])

    def _handleTags(self):
        self.all_sprites.empty()
        for tag in self._style:
            if tag == "MONSTER":
                shared.state.protag_mon.rect.center = (160, 128)
                self.all_sprites.add(shared.state.protag_mon)
            elif tag == "STOP_MUSIC":
                self._stopMixer()

    def _handleButton(self, prev_convo_key: str, index: int):
        """This function will handle any special case logic for clicking a button.
        This is called after loading in the next convo part but before rendering it.
        If this button leads to another mode, this is called before that.
        Should return True if moving to a new mode, False otherwise.
        """
        return False

    def _selectButton(self, index: int):
        button = self._choices[index]
        prev_convo_key = self._convo_key
        if button.key in self._convo_dict:
            self._convo_key = button.key
            self._loadText()
            changing_mode = self._handleButton(prev_convo_key, index)
            if not changing_mode:
                if self._convo_key != prev_convo_key:
                    self._resetPosition()
                self._renderText()
        else:
            next_mode = button.getNextMode()
            if next_mode:
                self._handleButton(prev_convo_key, index)
                self._stopMixer()
                self.next_mode = next_mode()
            else:
                raise ValueError(f"The convo mode {type(self).__name__}, at key {self._convo_key},"
                                 f"has a button that doesn't lead to anything: {index}")

    def _input(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.posSelect(event.pos, len(self._choices))
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self._read_text \
                    and self.posSelect(event.pos, len(self._choices)) is not None \
                    and self._mouseButtonStatus(event.button) \
                    and self.posSelect(self._mouseButtonStatus(event.button), len(self._choices)) \
                        == self.posSelect(event.pos, len(self._choices)):
                    self._selectButton(self._selected_button)
            elif event.button == 4:
                self._text_rect.move_ip(0, -constants.FONT_HEIGHT)
            elif event.button == 5:
                self._text_rect.move_ip(0, constants.FONT_HEIGHT)
        elif event.type == pygame.KEYDOWN and self._read_text:
            if event.key == pygame.K_RETURN:
                self._selectButton(self._selected_button)
            else:
                self.keySelect(event.key)

    @staticmethod
    def _getScrollDirection():
        pressed_keys = pygame.key.get_pressed()
        return (pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]) \
            - (pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w])

    def _update(self, dt):
        self._text_scroll, text_scroll_int = utility.getIntMovement(
            self._text_scroll,
            self._getScrollDirection() * self.SCROLL_AMOUNT_SPEED,
            dt
        )
        self._text_rect.move_ip(0, text_scroll_int)
        self._text_rect.clamp_ip(self._surf_text.get_rect())
        if self._text_rect.bottom >= self._surf_text.get_rect().bottom:
            self._read_text = True

    def _drawScreen(self, screen):
        screen.fill(constants.WHITE)
        screen.blit(self._background, (0, 0))
        screen.blit(self._surf_text, (12, 12), self._text_rect)
        if self._read_text:
            self.drawSelected(screen)
