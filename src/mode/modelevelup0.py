import constants
import shared

from .mode import Mode


class ModeLevelUp0(Mode):
    __slots__ = (
        'time',
    )

    def __init__(self):
        super().__init__()
        self.time = 0
        # self.all_sprites.add(star_sprite)
        # save current sprite from monster, level it up, and flicker between them
        # maybe some special effects too
        # maybe text? could have no text though

    def _input(self, event):
        pass

    def _update(self, dt):
        self.time += dt
        # keep track of timing

    def _drawScreen(self, screen):
        screen.fill(constants.WHITE)
