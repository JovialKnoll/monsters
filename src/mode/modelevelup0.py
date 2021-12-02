from .modelevelup import ModeLevelUp
from .modepostlevel0 import ModePostLevel0


class ModeLevelUp0(ModeLevelUp):
    def _switchMode(self):
        self.next_mode = ModePostLevel0()
