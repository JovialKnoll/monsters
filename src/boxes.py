class Boxes(object):
    elsewhere = pygame.Rect(0, 0, 320, 180)
    
    @staticmethod
    def textStart(box):
        return (box.x + 8, box.y + 8)
        
    @staticmethod
    def textWidth(box):
        return box.w - 16