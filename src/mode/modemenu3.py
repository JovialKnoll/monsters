import shared
from monster import Monster
from personality import Personality
from .modefight import ModeFight
from .modetalkwin3 import ModeTalkWin3
from .modetalkelse3 import ModeTalkElse3
from .modemenu import ModeMenu


class ModeMenu3(ModeMenu):
    def _handleButton(self, prev_convo_key, index):
        if prev_convo_key == "3aa":
            self._stopMixer()
            self.next_mode = ModeFight(
                shared.state.protag_mon,
                Monster.atLevel(3),
                lambda: ModeTalkWin3() if shared.state.fight_results[-1] == 1 else ModeTalkElse3()
            )
            return True
        return False
