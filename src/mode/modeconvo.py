import csv
import os
import copy

import pygame
import jovialengine

import constants
import mode
from .modebuttons import ModeButtons


class ConvoChoice(object):
    __slots__ = (
        'text',
        'key',
    )

    def __init__(self, text: str, key: str):
        self.text = text
        self.key = key

    def getNextMode(self):
        if hasattr(mode, self.key):
            mode_cls = getattr(mode, self.key)
            # currently only handling modes that can be created with no arguments
            return mode_cls
        return None


class ConvoPart(object):
    __slots__ = (
        'style',
        'text',
        'choices',
    )

    def __init__(self, style: set[str], text: str, choices: list[ConvoChoice]):
        self.style = style
        self.text = text
        self.choices = choices

    @staticmethod
    def getConvoDict(convo_file: str):
        convo_dict = {}
        with open(convo_file) as convo_data:
            convo_reader = csv.reader(convo_data)
            for row in convo_reader:
                row_iter = iter(row)
                key = next(row_iter)
                if key in convo_dict:
                    raise ValueError(f"The convo file {convo_file} has a duplicate row key {key}.")
                style = {tag.strip() for tag in next(row_iter).upper().split('|')}
                text = next(row_iter)
                choices = []
                try:
                    for i in range(len(ModeConvo.buttons)):
                        choice_text = next(row_iter)
                        choice_key = next(row_iter)
                        if choice_key:
                            choice = ConvoChoice(choice_text, choice_key)
                            choices.append(choice)
                except StopIteration:
                    pass
                if not choices:
                    raise ValueError(f"The convo file {convo_file} has no choices in the row with key {key}.")
                convo_part = ConvoPart(style, text, choices)
                convo_dict[key] = convo_part
        return convo_dict


class ModeConvo(ModeButtons, jovialengine.Saveable):
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
        '_active_tags',
        '_convo_dict',
        '_style',
        '_text',
        '_choices',
        '_read_text',
        '_text_rect',
        '_text_scroll',
        '_surf_text',
        '_user_interface',
    )

    def _keySelect(self, key):
        super()._keySelect(key)
        self._selected_button %= len(self._choices)

    def _posSelectButton(self, pos: tuple[int, int], index: int, rect: pygame.rect):
        if index >= len(self._choices):
            return None
        return super()._posSelectButton(pos, index, rect)

    def __init__(self, convo_key: str = '0'):
        super().__init__()
        self._background.fill(constants.WHITE)
        self._convo_key = convo_key
        self._active_tags = set()
        self._convo_dict = self._getScript()
        self._loadText()
        self._resetPosition()
        self._renderText()
        self._text_rect.clamp_ip(self._surf_text.get_rect())
        # in case of monster display
        jovialengine.shared.state.protag_mon.setImage()

    @classmethod
    def _getScript(cls):
        convo_file = os.path.join(
            constants.CONVO_DIRECTORY,
            cls.__name__.lower() + ".csv"
        )
        return ConvoPart.getConvoDict(convo_file)

    def save(self):
        return self._convo_key, self._active_tags

    @classmethod
    def load(cls, save_data):
        convo_key, active_tags = save_data
        new_obj = cls(convo_key)
        new_obj._style.update(active_tags)
        new_obj._renderText()
        return new_obj

    def _handleLoad(self):
        """This function will handle any special case logic for loading.
        This is called after loading in the next (or initial) convo part but before rendering it.
        This is called before any button specific logic.
        """
        pass

    @staticmethod
    def _getTextReplace():
        return {
            'MONSTER_NAME': jovialengine.shared.state.protag_mon.name,
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
        self._surf_text = jovialengine.shared.font_wrap.renderInside(296, self._text, False, constants.TEXT_COLOR)
        self._user_interface = pygame.image.load(constants.LAYOUT_1_FILE).convert()
        self._user_interface.set_colorkey(constants.COLORKEY)
        for index, button in enumerate(self._choices):
            jovialengine.shared.font_wrap.renderToInside(
                self._user_interface,
                self._textStart(index),
                self._textWidth(index),
                button.text,
                False,
                constants.TEXT_COLOR
            )
        for index in range(len(self._choices), 4):
            self._user_interface.fill(constants.WHITE, self.buttons[index])

    def _handleTags(self):
        self._all_sprites.empty()
        for tag in self._style:
            if tag == "SHOW_MONSTER":
                jovialengine.shared.state.protag_mon.rect.center = (160, 128)
                self._all_sprites.add(jovialengine.shared.state.protag_mon)
            elif tag == "START_CHAT_MUSIC":
                if "START_CHAT_MUSIC" not in self._active_tags:
                    pygame.mixer.music.load(constants.CHAT_LOOP)
                    pygame.mixer.music.play(-1)
                    self._active_tags.add("START_CHAT_MUSIC")
            elif tag == "STOP_MUSIC":
                self._stopMixer()
                self._active_tags.discard("START_CHAT_MUSIC")

    def _handleButton(self, prev_convo_key: str, index: int):
        """This function will handle any special case logic for clicking a button.
        This is called after loading in the next convo part but before rendering it.
        If this button leads to another mode, this is called before that.
        Should return True if moving to a new mode, False otherwise.
        """
        return False

    def _buttonPress(self):
        if not self._read_text:
            return
        button = self._choices[self._selected_button]
        prev_convo_key = self._convo_key
        if button.key in self._convo_dict:
            self._convo_key = button.key
            self._loadText()
            changing_mode = self._handleButton(prev_convo_key, self._selected_button)
            if changing_mode is None:
                raise ValueError(f"The convo mode {type(self).__name__} has a _handleButton function"
                                 f" that can return None. This should return either True or False.")
            if not changing_mode:
                if self._convo_key != prev_convo_key:
                    self._resetPosition()
                self._renderText()
        else:
            next_mode = button.getNextMode()
            if next_mode:
                self._handleButton(prev_convo_key, self._selected_button)
                self._stopMixer()
                self.next_mode = next_mode()
            else:
                raise ValueError(f"The convo mode {type(self).__name__}, at key {self._convo_key},"
                                 f" has a button that doesn't lead to anything: {self._selected_button}")

    def _input(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 4:
                self._text_rect.move_ip(0, -constants.FONT_HEIGHT)
            elif event.button == 5:
                self._text_rect.move_ip(0, constants.FONT_HEIGHT)
        super()._input(event)

    @staticmethod
    def _getScrollDirection():
        pressed_keys = pygame.key.get_pressed()
        return (pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]) \
            - (pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w])

    def _update(self, dt):
        self._text_scroll, text_scroll_int = jovialengine.utility.getIntMovement(
            self._text_scroll,
            self._getScrollDirection() * self.SCROLL_AMOUNT_SPEED,
            dt
        )
        self._text_rect.move_ip(0, text_scroll_int)
        self._text_rect.clamp_ip(self._surf_text.get_rect())
        if self._text_rect.bottom >= self._surf_text.get_rect().bottom:
            self._read_text = True

    def _drawPreSprites(self, screen):
        screen.blit(self._user_interface, (0, 0))
        screen.blit(self._surf_text, (12, 12), self._text_rect)
        if self._read_text:
            self._drawSelected(screen)
