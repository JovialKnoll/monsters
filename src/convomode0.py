from monconvomode import *
from testmode import *
from fightmode import *
from monster import *
class ConvoMode0(MonConvoMode):
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
    def _textButton0(self):
        return "Go, to TestMode!"
    def _textButton1(self):
        return "012345678 012345678"
    def _textButton2(self):
        return "Content~"
    def _textButton3(self):
        return "Excited!"
    def _goButton0(self):
        print "Button 0 was pressed."
        self.next_mode = TestMode()
    def _goButton1(self):
        print "Really anything can happen here."
        self.next_mode = FightMode(self.shared['protag_mon'], Monster.atLevel(1))
    def _goButton2(self):
        print "The main thing would be to have pressing a button set variables."
    def _goButton3(self):
        print "The other main thing would be to have pressing a button change the mode.\n" + \
            "It could set variables and then change the mode."
    #__init__ need not be implemented unless adding things
    #if adding things to init, should start as below
    #def __init__(self):
    #    super(ConvoMode0, self).__init__()
        