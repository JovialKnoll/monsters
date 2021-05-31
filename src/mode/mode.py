import abc
import typing

import pygame


class Mode(abc.ABC):
    """This is an abstract object for game modes.
    """
    __slots__ = (
        'all_sprites',
        '__pressed_mouse_buttons',
        'next_mode',
    )

    def __init__(self):
        """All game modes must set the next mode when they are done.
        Don't create another mode unless you are immediately assigning it to self.next_mode
        """
        self.all_sprites = pygame.sprite.LayeredDirty()
        self.__pressed_mouse_buttons = dict()
        self.next_mode = None

    def __trackMouseButton(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.__pressed_mouse_buttons[event.button] = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in self.__pressed_mouse_buttons:
                del self.__pressed_mouse_buttons[event.button]

    def _mouseButtonStatus(self, button: int):
        if button not in self.__pressed_mouse_buttons:
            return False
        return self.__pressed_mouse_buttons[button]

    @abc.abstractmethod
    def _input(self, event: pygame.event.Event):
        raise NotImplementedError(
            type(self).__name__ + "._input(self, event)"
        )

    @typing.final
    def input_events(self, events: list[pygame.event.Event]):
        """All game modes can take in events."""
        for event in events:
            self._input(event)
            self.__trackMouseButton(event)

    def _update(self, dt: int):
        pass

    @typing.final
    def update(self, dt: int):
        """All game modes can update."""
        self._update(dt)
        self.all_sprites.update(dt)

    @abc.abstractmethod
    def _drawScreen(self, screen: pygame.surface.Surface):
        raise NotImplementedError(
            type(self).__name__ + "._drawScreen(self, screen)"
        )

    def _drawPostSprites(self, screen: pygame.surface.Surface):
        pass

    @typing.final
    def draw(self, screen: pygame.surface.Surface):
        """All game modes can draw to the screen"""
        self._drawScreen(screen)
        self.all_sprites.draw(screen)
        self._drawPostSprites(screen)

    @staticmethod
    def _stopMixer():
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.stop()
