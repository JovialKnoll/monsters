import jovialengine

from monster import Monster
from .modefight import ModeFight
from .modetalkwin3 import ModeTalkWin3
from .modeconvo import ModeConvo


class ModeTalkElse3(ModeConvo):
    def _handleButton(self, prev_convo_key: str, index: int):
        if prev_convo_key == "1":
            self._stopMixer()
            self.next_mode = ModeFight(
                jovialengine.shared.state.protag_mon,
                Monster.atLevel(3),
                lambda: ModeTalkWin3() if jovialengine.shared.state.fight_results[-1] == 1 else ModeTalkElse3()
            )
            return True
        return False
