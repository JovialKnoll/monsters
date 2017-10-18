import os
import pickle

import pygame

import constants
import shared
from gamemode import GameMode

class GameMenuMode(GameMode):
    class State(object):
        Menu, Save, Load = range(3)
    menu_width = 20
    file_extension = '.sav'
    def __init__(self, previous_mode):
        super(GameMenuMode, self).__init__()
        self.state = GameMenuMode.State.Menu
        self.previous_mode = previous_mode
        self.old_screen = pygame.Surface(constants.SCREEN_SIZE).convert(shared.display.screen)
        previous_mode._drawScreen(self.old_screen)

    def _resetCursorBlink(self):
        self.cursor_switch = True
        self.cursor_timer = 0

    def _clearSaveStuff(self):
        self.save_name = ''
        self.cursor_position = 0
        self._resetCursorBlink()

    def _saveGame(self):
        """Save the game."""
        objects = ['asd', (1,2,3), 123]
        if not os.path.exists(constants.SAVE_DIRECTORY):
            os.makedirs(constants.SAVE_DIRECTORY)
        with open(
            os.path.join(
                constants.SAVE_DIRECTORY,
                self.save_name + self.__class__.file_extension
            ),
            'wb'
        ) as f:
            pickle.dump(objects, f, pickle.HIGHEST_PROTOCOL)

    def _inputMenu(self, event):
        if event.type == pygame.QUIT:
            shared.game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_mode = self.previous_mode
            elif event.key == pygame.K_F1:
                self._clearSaveStuff()
                self.state = GameMenuMode.State.Save
            elif event.key == pygame.K_F2:
                self._clearSaveStuff()
                self.state = GameMenuMode.State.Load
            elif event.key == pygame.K_F3:
                shared.game_running = False

    def _inputSave(self, event):
        if event.type == pygame.QUIT:
            self.state = GameMenuMode.State.Menu
        elif event.type == pygame.KEYDOWN:
            char = event.unicode
            length = len(self.save_name)
            if event.key == pygame.K_ESCAPE:
                self.state = GameMenuMode.State.Menu
            elif event.key == pygame.K_RETURN:
            # also call on a button press
                if self.save_name:
                    self._saveGame()
                    self.state = GameMenuMode.State.Menu
            elif event.key == pygame.K_LEFT:
                self.cursor_position = max(self.cursor_position - 1, 0)
                self._resetCursorBlink()
            elif event.key == pygame.K_RIGHT:
                self.cursor_position = min(self.cursor_position+1, length)
                self._resetCursorBlink()
            elif event.key in (pygame.K_UP, pygame.K_HOME):
                self.cursor_position = 0
                self._resetCursorBlink()
            elif event.key in (pygame.K_DOWN, pygame.K_END):
                self.cursor_position = length
                self._resetCursorBlink()
            elif event.key == pygame.K_DELETE:
                self.save_name = self.save_name[:self.cursor_position] + self.save_name[self.cursor_position+1:]
                self._resetCursorBlink()
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_position > 0:
                    self.save_name = self.save_name[:self.cursor_position-1] + self.save_name[self.cursor_position:]
                    self.cursor_position -= 1
                self._resetCursorBlink()
            elif (
                length < (self.__class__.menu_width - len(self.__class__.file_extension))
                and (
                    # numbers
                    (char >= '0' and char <= '9' )
                    # or letters
                    or (event.key > 96 and event.key < 123)
                )
            ):
                self.save_name = self.save_name[:self.cursor_position] + char + self.save_name[self.cursor_position:]
                self.cursor_position += 1
                self._resetCursorBlink()

    def _inputLoad(self, event):
        if event.type == pygame.QUIT:
            self.state = GameMenuMode.State.Menu
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = GameMenuMode.State.Menu
            # put in scrolling to select save file? maybe typing too? alphebatized list...

    def _input(self, event):
        if self.state is GameMenuMode.State.Menu:
            self._inputMenu(event)
        elif self.state is GameMenuMode.State.Save:
            self._inputSave(event)
        elif self.state is GameMenuMode.State.Load:
            self._inputLoad(event)
        else:
            raise RuntimeError("error: self.state = " + str(self.state))

    def update(self):
        if self.state is GameMenuMode.State.Menu:
            pass
        elif self.state is GameMenuMode.State.Save:
            if self.cursor_timer >= constants.CURSOR_TIME:
                self.cursor_switch = not self.cursor_switch
                self.cursor_timer = 0
            self.cursor_timer += 1
        elif self.state is GameMenuMode.State.Load:
            pass
        else:
            raise RuntimeError("error: self.state = " + str(self.state))

    def _drawScreen(self, screen):
        screen.blit(self.old_screen, (0,0))
        if self.state is GameMenuMode.State.Menu:
            disp_text = "Options:\n_Go Back (ESC)\n_Save (F1)\n_Load (F2)\n_Quit (F3)"
            shared.font_wrap.renderToInside(
                screen,
                (0,0),
                self.__class__.menu_width * constants.FONT_SIZE,
                disp_text,
                False,
                constants.WHITE,
                constants.BLACK
            )
            # center this, make bigger and buttons... maybe
            # more to come
        elif self.state is GameMenuMode.State.Save:
            disp_text = "Options:\n_Go Back (ESC)\n_Save (ENTER)\nType a file name:\n"
            if self.save_name:
                disp_text += self.save_name
            disp_text += self.__class__.file_extension
            shared.font_wrap.renderToInside(
                screen,
                (0,0),
                self.__class__.menu_width * constants.FONT_SIZE,
                disp_text,
                False,
                constants.WHITE,
                constants.BLACK
            )
            if self.cursor_switch:
                screen.fill(
                    constants.WHITE,
                    ((self.cursor_position * constants.FONT_SIZE, 4 * constants.FONT_HEIGHT), (1, constants.FONT_HEIGHT))
                )
            # display prompt for file to save
            # display save_name in there
        elif self.state is GameMenuMode.State.Load:
            disp_text = "Options:\n_Go Back (ESC)\n_Load (ENTER)\nSelect a file name:\n"
            disp_text += self.__class__.file_extension
            shared.font_wrap.renderToInside(
                screen,
                (0,0),
                self.__class__.menu_width * constants.FONT_SIZE,
                disp_text,
                False,
                constants.WHITE,
                constants.BLACK
            )
            # draw load thingy
            pass
        else:
            raise RuntimeError("error: self.state = " + str(self.state))
