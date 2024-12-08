import jovialengine

from sprite import Monster
from .modefight import ModeFight
from .modetalkwin2 import ModeTalkWin2
from .modeconvo import ModeConvo


class ModeTalkElse2(ModeConvo):
    def _handle_button(self, prev_convo_key: str, index: int):
        if prev_convo_key == "2":
            self._stop_mixer()
            self.next_mode = ModeFight(
                jovialengine.get_state().protag_mon,
                Monster.at_level(2),
                lambda: ModeTalkWin2() if jovialengine.get_state().fight_results[-1] == 1 else ModeTalkElse2()
            )
            return True
        return False
