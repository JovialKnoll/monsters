import jovialengine

from sprite import Monster
from .modefight import ModeFight
from .modetalkwin3 import ModeTalkWin3
from .modeconvo import ModeConvo


class ModeTalkElse3(ModeConvo):
    def _handle_button(self, prev_convo_key: str, index: int):
        if prev_convo_key == "1":
            self._stop_mixer()
            self.next_mode = ModeFight(
                jovialengine.get_state().protag_mon,
                Monster.at_level(3),
                lambda: ModeTalkWin3() if jovialengine.get_state().fight_results[-1] == 1 else ModeTalkElse3()
            )
            return True
        return False
