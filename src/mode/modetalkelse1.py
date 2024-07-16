import jovialengine

from monster import Monster
from .modefight import ModeFight
from .modetalkwin1 import ModeTalkWin1
from .modeconvo import ModeConvo


class ModeTalkElse1(ModeConvo):
    def _handle_button(self, prev_convo_key: str, index: int):
        if prev_convo_key == "4a":
            self._stop_mixer()
            self.next_mode = ModeFight(
                jovialengine.get_state().protag_mon,
                Monster.at_level(1),
                lambda: ModeTalkWin1() if jovialengine.get_state().fight_results[-1] == 1 else ModeTalkElse1()
            )
            return True
        return False
