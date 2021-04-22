import abc

import pygame


class Mode(abc.ABC):
    """This is an abstract object for game modes.
    """
    __slots__ = (
        'all_sprites',
        '__pressed_keys',
        '__pressed_mouse_buttons',
        'next_mode',
    )

    def __init__(self):
        """All game modes must set the next mode when they are done."""
        self.all_sprites = pygame.sprite.LayeredDirty()
        self.__pressed_keys = set()
        self.__pressed_mouse_buttons = dict()
        self.next_mode = None

    def saveMode(self):
        raise NotImplementedError(
            self.__class__.__name__ + ".saveMode(self)"
        )

    @classmethod
    def loadMode(cls, saveData):
        raise NotImplementedError(
            cls.__name__ + ".loadMode(cls, saveData)"
        )

    def __trackPressedKeys(self, event):
        if event.type == pygame.KEYDOWN:
            self.__pressed_keys.add(event.key)
        elif event.type == pygame.KEYUP:
            self.__pressed_keys.discard(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.__pressed_mouse_buttons[event.button] = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in self.__pressed_mouse_buttons:
                del self.__pressed_mouse_buttons[event.button]

    def _keyStatus(self, key):
        return key in self.__pressed_keys

    def _mouseButtonStatus(self, button):
        if button not in self.__pressed_mouse_buttons:
            return False
        return self.__pressed_mouse_buttons[button]

    @abc.abstractmethod
    def _input(self, event):
        raise NotImplementedError(
            self.__class__.__name__ + "._input(self, event)"
        )

    def input_events(self, event_list):
        """All game modes can take in events."""
        for event in event_list:
            self._input(event)
            self.__trackPressedKeys(event)

    def _update(self, dt):
        pass

    def update(self, dt):
        """All game modes can update."""
        self._update(dt)
        self.all_sprites.update(dt)

    @abc.abstractmethod
    def _drawScreen(self, screen):
        raise NotImplementedError(
            self.__class__.__name__ + "._drawScreen(self, screen)"
        )

    def _drawPostSprites(self, screen):
        pass

    def draw(self, screen):
        """All game modes can draw to the screen"""
        self._drawScreen(screen)
        self.all_sprites.draw(screen)
        self._drawPostSprites(screen)
