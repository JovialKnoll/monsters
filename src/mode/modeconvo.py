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

    def get_next_mode(self):
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
    def get_convo_dict(convo_file: str):
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

    def _key_select(self, change):
        super()._key_select(change)
        self._selected_button %= len(self._choices)

    def _pos_select_button(self, pos: tuple[int, int], index: int, rect: pygame.rect):
        if index >= len(self._choices):
            return None
        return super()._pos_select_button(pos, index, rect)

    def __init__(self, convo_key: str = '0'):
        super().__init__()
        self._background.fill(constants.WHITE)
        self._convo_key = convo_key
        self._active_tags = set()
        self._convo_dict = self._get_script()
        self._load_text()
        self._reset_position()
        self._render_text()
        self._text_rect.clamp_ip(self._surf_text.get_rect())
        # in case of monster display
        jovialengine.get_state().protag_mon.set_image()

    @classmethod
    def _get_script(cls):
        convo_file = os.path.join(
            constants.CONVO_DIRECTORY,
            cls.__name__.lower() + ".csv"
        )
        return ConvoPart.get_convo_dict(convo_file)

    def save(self):
        return self._convo_key, self._active_tags

    @classmethod
    def load(cls, save_data):
        convo_key, active_tags = save_data
        new_obj = cls(convo_key)
        new_obj._style.update(active_tags)
        new_obj._render_text()
        return new_obj

    def _handle_load(self):
        """This function will handle any special case logic for loading.
        This is called after loading in the next (or initial) convo part but before rendering it.
        This is called before any button specific logic.
        """
        pass

    @staticmethod
    def _get_text_replace():
        return {
            'MONSTER_NAME': jovialengine.get_state().protag_mon.name,
        }

    def _load_text(self):
        convo_part = self._convo_dict[self._convo_key]
        # copy so that alterations don't affect basis
        self._style = copy.copy(convo_part.style)
        self._text = convo_part.text.format(**self._get_text_replace())
        self._choices = copy.copy(convo_part.choices)
        self._handle_load()

    def _reset_position(self):
        self._read_text = False
        self._text_rect = pygame.Rect(0, 0, 296, 56)
        self._text_scroll = 0
        self._selected_button = 0

    def _render_text(self):
        self._handle_tags()
        self._surf_text = jovialengine.get_default_font_wrap().render_inside(
            296,
            self._text,
            constants.TEXT_COLOR,
            constants.WHITE
        )
        self._user_interface = jovialengine.load.image(constants.LAYOUT_1_FILE, constants.COLORKEY).copy()
        for index, button in enumerate(self._choices):
            jovialengine.get_default_font_wrap().render_to_inside(
                self._user_interface,
                self._text_start(index),
                self._text_width(index),
                button.text,
                constants.TEXT_COLOR
            )
        for index in range(len(self._choices), 4):
            self._user_interface.fill(constants.WHITE, self.buttons[index])

    def _handle_tags(self):
        self.sprite_groups["all"].empty()
        for tag in self._style:
            if tag == "SHOW_MONSTER":
                jovialengine.get_state().protag_mon.rect.center = (160, 128)
                self.sprite_groups["all"].add(jovialengine.get_state().protag_mon)
            elif tag == "START_CHAT_MUSIC":
                if "START_CHAT_MUSIC" not in self._active_tags:
                    pygame.mixer.music.load(constants.CHAT_LOOP)
                    pygame.mixer.music.play(-1)
                    self._active_tags.add("START_CHAT_MUSIC")
            elif tag == "STOP_MUSIC":
                self._stop_mixer()
                self._active_tags.discard("START_CHAT_MUSIC")

    def _handle_button(self, prev_convo_key: str, index: int):
        """This function will handle any special case logic for clicking a button.
        This is called after loading in the next convo part but before rendering it.
        If this button leads to another mode, this is called before that.
        Should return True if moving to a new mode, False otherwise.
        """
        return False

    def _button_press(self):
        if not self._read_text:
            return
        button = self._choices[self._selected_button]
        prev_convo_key = self._convo_key
        if button.key in self._convo_dict:
            self._convo_key = button.key
            self._load_text()
            changing_mode = self._handle_button(prev_convo_key, self._selected_button)
            if changing_mode is None:
                raise ValueError(f"The convo mode {type(self).__name__} has a _handleButton function"
                                 f" that can return None. This should return either True or False.")
            if not changing_mode:
                if self._convo_key != prev_convo_key:
                    self._reset_position()
                self._render_text()
        else:
            next_mode = button.get_next_mode()
            if next_mode:
                self._handle_button(prev_convo_key, self._selected_button)
                self._stop_mixer()
                self.next_mode = next_mode()
            else:
                raise ValueError(f"The convo mode {type(self).__name__}, at key {self._convo_key},"
                                 f" has a button that doesn't lead to anything: {self._selected_button}")

    def _take_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 4:
                self._text_rect.move_ip(0, -constants.FONT_HEIGHT)
            elif event.button == 5:
                self._text_rect.move_ip(0, constants.FONT_HEIGHT)
        super()._take_event(event)

    def _get_scroll_direction(self):
        return (self._input_frame.get_input_state(0, constants.EVENT_DOWN)) \
            - (self._input_frame.get_input_state(0, constants.EVENT_UP))

    def _update(self, dt):
        self._text_scroll, text_scroll_int = jovialengine.utility.get_int_movement(
            self._text_scroll,
            self._get_scroll_direction() * self.SCROLL_AMOUNT_SPEED,
            dt
        )
        self._text_rect.move_ip(0, text_scroll_int)
        self._text_rect.clamp_ip(self._surf_text.get_rect())
        if self._text_rect.bottom >= self._surf_text.get_rect().bottom:
            self._read_text = True

    def _draw_pre_sprites(self, screen):
        screen.blit(self._user_interface, (0, 0))
        screen.blit(self._surf_text, (12, 12), self._text_rect)
        if self._read_text:
            self._draw_selected(screen)
