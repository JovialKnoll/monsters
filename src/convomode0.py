from convomode import *
from testmode import *
class ConvoMode0(ConvoMode):
    def _goButton0(self):
        print "Button 0 was pressed."
        self.next_mode = TestMode()
    def _goButton1(self):
        print "Really anything can happen here."
    def _goButton2(self):
        print "The main thing would be to have pressing a button set variables."
    def _goButton3(self):
        print "The other main thing would be to have pressing a button change the mode.\n" + \
            "It could set variables and then change the mode."
    def _setText(self):
        self.text = "Scrolling is enabled!\n" + \
            "Try pressing the arrow keys!\n" + \
            "Up and down to scroll, left and right to select.\n" + \
            "This is the test conversation section.\n" + \
            "How do you feel about that?\n" + \
            "a\n" + \
            "b\n" + \
            "c\n" + \
            "d\n" + \
            "e\n"
        self.text0 = "Go, to TestMode!"
        self.text1 = "012345678 012345678"
        self.text2 = "Content~"
        self.text3 = "Excited!"
        
    #__init__ need not be implemented unless adding things
    #if adding things to init, should start as below
    #def __init__(self):
    #    super(ConvoMode0, self).__init__()
        