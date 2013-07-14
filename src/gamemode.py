class GameMode(object):
    """This is an abstract object for game modes.
    Children of this should implement input, update, and draw.
    """
    def __init__(self):
        """All game modes must when they are done.be aware of the shared dictionary."""
        self.done = False
        
    def input(self, event_list):
        raise NotImplementedError("Implement: GameMode.input.")
        
    def update(self):
        raise NotImplementedError("Implement: GameMode.update.")
        
    def draw(self, screen):
        raise NotImplementedError("Implement: GameMode.draw.")
        