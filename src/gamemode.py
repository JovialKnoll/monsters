class GameMode(object):
    """This is an abstract object for game modes.
    Children of this should implement input, update, and draw.
    """
    def __init__(self, screen_size, shared_dict):
        """All game modes must be aware of screen size and the shared dictionary."""
        self.done = False
        self.SCREEN_SIZE = screen_size
        self.shared_dict = shared_dict
        
    def input(self, event_list):
        raise NotImplementedError("Implement: input.")
        
    def update(self):
        raise NotImplementedError("Implement: update.")
        
    def draw(self, screen):
        raise NotImplementedError("Implement: draw.")
        