from .modepostlevel2 import ModePostLevel2
from .modelevelup import ModeLevelUp


class ModeLevelUp2(ModeLevelUp):
    def _switchMode(self):
        self.next_mode = ModePostLevel2()
