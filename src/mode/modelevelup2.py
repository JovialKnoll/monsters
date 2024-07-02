from .modepostlevel2 import ModePostLevel2
from .modelevelup import ModeLevelUp


class ModeLevelUp2(ModeLevelUp):
    def _switch_mode(self):
        self.next_mode = ModePostLevel2()
