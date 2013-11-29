from gamemode import *
from monster import *
from constants import *
class TestMode(GameMode):
    def _createMonster(self):
        self.shared['protag_mon'] = Monster()
        self.test_mon_pos = [160,122]
        
    def __init__(self):
        super(TestMode, self).__init__()
        self.fill = (0, 200, 0)
        self._createMonster()
        self.move_dict = {'left': 0, 'right': 0, 'up': 0, 'down': 0}
        self.test_text = "01234567890123456789"
        
    def input(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._createMonster()
                elif event.key == pygame.K_l:
                    self.shared['protag_mon'].levelUp()
                elif event.key == pygame.K_LEFT:
                    self.move_dict['left'] = 1
                elif event.key == pygame.K_RIGHT:
                    self.move_dict['right'] = 1
                elif event.key == pygame.K_UP:
                    self.move_dict['up'] = 1
                elif event.key == pygame.K_DOWN:
                    self.move_dict['down'] = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.move_dict['left'] = 0
                elif event.key == pygame.K_RIGHT:
                    self.move_dict['right'] = 0
                elif event.key == pygame.K_UP:
                    self.move_dict['up'] = 0
                elif event.key == pygame.K_DOWN:
                    self.move_dict['down'] = 0
            elif event.type == pygame.MOUSEMOTION:
                self.test_mon_pos = list(event.pos)
                    
    def update(self):
        self.test_mon_pos[0] += self.move_dict['right'] - self.move_dict['left']
        self.test_mon_pos[1] += self.move_dict['down'] - self.move_dict['up']
        
    def draw(self, screen):
        #clear of old draws
        screen.fill(self.fill)
        #make new draws
        self.shared['protag_mon'].drawStanding(screen, self.test_mon_pos)
        self.shared['font_wrap'].renderToInside(screen, (0,0), self.shared['SCREEN_SIZE'][0]//2, self.test_text, False, BLACK, WHITE)
        self.shared['font_wrap'].renderToInside(screen, (self.shared['SCREEN_SIZE'][0]//2,0), self.shared['SCREEN_SIZE'][0]//2, "Lorem", False, (255,0,0))
        #screen.blit(self.shared['font_wrap'].renderInside(self.shared['SCREEN_SIZE'][0]//2, self.test_text, False, BLACK, WHITE), (0,0))
        #screen.blit(self.shared['font_wrap'].renderInside(self.shared['SCREEN_SIZE'][0]//2, "Lorem", False, (255,0,0)), (self.shared['SCREEN_SIZE'][0]//2,0))
        