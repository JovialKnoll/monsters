import shared
from monster import Monster

from .modeconvo import ModeConvo


class ModeIntroduction0(ModeConvo):
    def _handleButton(self, prev_convo_key: str, index: int):
        if prev_convo_key == '2' and index == 0:
            shared.state.protag_mon = Monster()
