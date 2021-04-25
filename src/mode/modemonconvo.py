import shared
from .modeconvo import ModeConvo


class ModeMonConvo(ModeConvo):
    __slots__ = (
    )

    def __init__(self):
        super(ModeMonConvo, self).__init__()
        shared.state.protag_mon.rect.center = (160, 128)
        self.all_sprites.add(shared.state.protag_mon)
