from .modepostlevel0 import ModePostLevel0
from .modelevelup import ModeLevelUp


class ModeLevelUp0(ModeLevelUp):
    def _switch_mode(self):
        self.next_mode = ModePostLevel0()
