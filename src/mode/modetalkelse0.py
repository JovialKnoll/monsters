import jovialengine

from monster import Monster
from .modefight import ModeFight
from .modetalkwin0 import ModeTalkWin0
from .modeconvo import ModeConvo


class ModeTalkElse0(ModeConvo):
    def _handleButton(self, prev_convo_key: str, index: int):
        if prev_convo_key == "6":
            self._stopMixer()
            self.next_mode = ModeFight(
                jovialengine.game.getInstance().state.protag_mon,
                Monster.atLevel(0),
                lambda: ModeTalkWin0() if jovialengine.game.getInstance().state.fight_results[-1] == 1 else ModeTalkElse0()
            )
            return True
        return False
