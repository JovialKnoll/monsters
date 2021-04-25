import shared
from monster import Monster

from .modemonconvo import ModeMonConvo
from .modetest import ModeTest
from .modefight import ModeFight
from .modemenu import ModeMenu


class ModeMonConvo0(ModeMonConvo):
    __slots__ = (
    )

    def _textMain(self):
        return "Scrolling is enabled!\n" + \
            "Try pressing the arrow keys!\n" + \
            "Up and down to scroll, left and right to select.\n" + \
            "This is the test conversation section.\n" + \
            "How do you feel about that?\n" + \
            "a\n" + \
            "b\n" + \
            "c\n" + \
            "d\n" + \
            "e\n"

    def _textButton(self, index):
        if index == 0:
            return "Go, to ModeTest!"
        elif index == 1:
            return "Go, to ModeFight"
        elif index == 2:
            return "Content~"
        elif index == 3:
            return "Excited!"

    def _goButton(self, index):
        if index == 0:
            print("Button 0 was pressed.")
            self.next_mode = ModeTest()
        elif index == 1:
            print("Really anything can happen here.")
            self.next_mode = ModeFight(
                shared.state.protag_mon,
                Monster.atLevel(0),
                ModeMonConvo0,
                ModeMonConvo0,
                ModeTest
            )
        elif index == 2:
            print("The main thing would be to have pressing a button set variables.")
            self.next_mode = ModeMenu()
        elif index == 3:
            print("The other main thing would be to have pressing a button change the mode.\n"
                + "It could set variables and then change the mode.")
    # __init__ need not be implemented unless adding things
    # if adding things to init, should start as below
    # def __init__(self):
    #     super(ModeMonConvo0, self).__init__()
