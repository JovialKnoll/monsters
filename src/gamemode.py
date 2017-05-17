class GameMode(object):
    """This is an abstract object for game modes.
    Children of this should implement input, update, and draw.
    """
    shared = {}
    def __init__(self):
        """All game modes must know when they are done, and set the next mode."""
        self.next_mode = False

    def input(self, event_list):
        """All game modes can take in events."""
        raise NotImplementedError(self.__class__.__name__ + ".input(self, event_list)")

    def update(self):
        """All game modes can update and can optionally return True to halt the game."""
        raise NotImplementedError(self.__class__.__name__ + ".update(self)")

    def draw(self, screen):
        """All game modes can draw to the screen"""
        raise NotImplementedError(self.__class__.__name__ + ".draw(self, screen)")
