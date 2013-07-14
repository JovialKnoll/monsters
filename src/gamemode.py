class GameMode(object):
    """This is an abstract object for game modes.
    Children of this should implement input, update, and draw.
    """
    def __init__(self):
        """All game modes must when they are done.be aware of the shared dictionary."""
        self.done = False
        
    def input(self, event_list):
        raise NotImplementedError(self.__class__.__name__ + ".input(self, event_list)")
        
    def update(self):
        raise NotImplementedError(self.__class__.__name__ + ".update(self)")
        
    def draw(self, screen):
        raise NotImplementedError(self.__class__.__name__ + ".draw(self, screen)")
        