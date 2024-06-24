import jovialengine

from monster import Monster
from .modefight import ModeFight
from .modetalkwin0 import ModeTalkWin0
from .modeconvo import ModeConvo


class ModeTalkElse0(ModeConvo):
    def _handleButton(self, prev_convo_key: str, index: int):
        if prev_convo_key == "6":
            self._stop_mixer()
            self.next_mode = ModeFight(
                jovialengine.get_game().state.protag_mon,
                Monster.atLevel(0),
                lambda: ModeTalkWin0() if jovialengine.get_game().state.fight_results[-1] == 1 else ModeTalkElse0()
            )
            return True
        return False
