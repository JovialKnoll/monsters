from .modepostlevel1 import ModePostLevel1
from .modelevelup import ModeLevelUp


class ModeLevelUp1(ModeLevelUp):
    def _switch_mode(self):
        self.next_mode = ModePostLevel1()
