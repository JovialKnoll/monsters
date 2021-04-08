import pygame

import shared

class Mode(object):
    """This is an abstract object for game modes.
    Children of this should implement _input, update, and draw.
    """
    __slots__ = (
        'all_sprites',
        '__pressed_keys',
        'next_mode',
    )

    def __init__(self):
        """All game modes must set the next mode when they are done."""
        self.all_sprites = pygame.sprite.LayeredDirty()
        self.__pressed_keys = set()
        self.next_mode = None

    def __trackPressedKeys(self, event):
        if event.type == pygame.KEYDOWN:
            self.__pressed_keys.add(event.key)
        elif event.type == pygame.KEYUP:
            self.__pressed_keys.discard(event.key)

    def _keyStatus(self, key):
        return key in self.__pressed_keys

    def _input(self, event):
        raise NotImplementedError(
            self.__class__.__name__ + "._input(self, event)"
        )

    def input_events(self, event_list):
        """All game modes can take in events."""
        for event in event_list:
            self.__trackPressedKeys(event)
            self._input(event)

    def _update(self, dt):
        pass

    def update(self, dt):
        """All game modes can update."""
        self._update(dt)
        self.all_sprites.update(dt)

    def _drawScreen(self, screen):
        raise NotImplementedError(
            self.__class__.__name__ + "._drawScreen(self, screen)"
        )

    def draw(self, screen=shared.display.screen):
        """All game modes can draw to the screen"""
        self._drawScreen(screen)
        self.all_sprites.draw(screen)
