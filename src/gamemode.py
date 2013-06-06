class GameMode(object):
    """This is an abstract object for game modes.
    Children of this should implement input, update, and draw.
    """
    def __init__(self, shared):
        """All game modes must be aware of the shared dictionary."""
        self.done = False
        self.shared = shared
        
    def input(self, event_list):
        raise NotImplementedError("Implement: input.")
        
    def update(self):
        raise NotImplementedError("Implement: update.")
        
    def draw(self, screen):
        raise NotImplementedError("Implement: draw.")
        