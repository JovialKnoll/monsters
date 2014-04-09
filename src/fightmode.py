import os, pygame, random, utility
from gamemode import *
from boxes import *
from constants import *
from collections import deque
random.seed()
class FightMode(GameMode):
    class FightBoxes(Boxes):
        rects = {
            'top'   : pygame.Rect(24,  24,  88,  36),
            'middle': pygame.Rect(24,  76,  88,  36),
            'bottom': pygame.Rect(24, 128,  88,  36),
        }
        
        @classmethod
        def boxKey(cls, box, key):
            """Return a rectangle based on the current rectangle and the key pressed."""
            if (box is cls.rects['middle'] and key in (  pygame.K_UP,  pygame.K_LEFT))\
            or (box is cls.rects['bottom'] and key in (pygame.K_DOWN, pygame.K_RIGHT)):
                return cls.rects[   'top']
            if (box is cls.rects['bottom'] and key in (  pygame.K_UP,  pygame.K_LEFT))\
            or (box is cls.rects[   'top'] and key in (pygame.K_DOWN, pygame.K_RIGHT)):
                return cls.rects['middle']
            if (box is cls.rects[   'top'] and key in (  pygame.K_UP,  pygame.K_LEFT))\
            or (box is cls.rects['middle'] and key in (pygame.K_DOWN, pygame.K_RIGHT)):
                return cls.rects['bottom']
            return box
            
    black_box = pygame.image.load(os.path.join('gfx', 'backgrounds', 'blackbox.png'))
    background = pygame.image.load(os.path.join('gfx', 'backgrounds', 'layout2boxes.png'))
    converted = False
    
    def __init__(self, player_mon, enemy_mon):
        super(FightMode, self).__init__()
        if not FightMode.converted:
            FightMode.black_box = FightMode.black_box.convert_alpha()
            FightMode.shared['font_wrap'].renderToInside(FightMode.background,
                FightMode.FightBoxes.textStart(   FightMode.FightBoxes.rects['top']),
                FightMode.FightBoxes.textWidth(   FightMode.FightBoxes.rects['top']),
                "Attack", False, TEXT_COLOR
            )
            FightMode.shared['font_wrap'].renderToInside(FightMode.background,
                FightMode.FightBoxes.textStart(FightMode.FightBoxes.rects['middle']),
                FightMode.FightBoxes.textWidth(FightMode.FightBoxes.rects['middle']),
                "Defend", False, TEXT_COLOR
            )
            FightMode.shared['font_wrap'].renderToInside(FightMode.background,
                FightMode.FightBoxes.textStart(FightMode.FightBoxes.rects['bottom']),
                FightMode.FightBoxes.textWidth(FightMode.FightBoxes.rects['bottom']),
                "Escape", False, TEXT_COLOR
            )
            FightMode.background = FightMode.background.convert_alpha()
            FightMode.converted = True
        self.box_selected = FightMode.FightBoxes.rects['top']
        
        player_mon.fightStart()
        self.player_mon = player_mon
        self.enemy_mon = enemy_mon
        
        self.player_pos = (170,128)
        self.enemy_pos = (262,128)
        self.player_rel = [0,0]
        self.enemy_rel = [0,0]
        
        self.player_action = False
        self.enemy_action = False
        self.player_anim = 0
        self.enemy_anim = 0
        
        self.action_display = deque((), 4)
        self.action_set = False
        
    def _buttonPress(self):
        if self.box_selected == FightMode.FightBoxes.rects['top']:
            self.player_action = 'attack'
            #print "pressed: top"
        elif self.box_selected == FightMode.FightBoxes.rects['middle']:
            self.player_action = 'defend'
            #print "pressed: middle"
        elif self.box_selected == FightMode.FightBoxes.rects['bottom']:
            self.player_action = 'escape'
            #print "pressed: bottom"
        self.enemy_action = random.choice(('attack', 'defend'))
            
    def input(self, event_list):
        if self.player_action:
            return
        for event in event_list:
            if event.type == pygame.MOUSEMOTION:
                select = FightMode.FightBoxes.boxIn(event.pos)
                if select != FightMode.FightBoxes.elsewhere:
                    self.box_selected = select
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    select = FightMode.FightBoxes.boxIn(event.pos)
                    if select != FightMode.FightBoxes.elsewhere:
                        self.box_selected = select
                        self._buttonPress()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    print "player_mon.stats = "+str(self.player_mon.stats)
                    print "enemy_mon.stats = "+str(self.enemy_mon.stats)
                if event.key == pygame.K_RETURN:
                    self._buttonPress()
                else:
                    self.box_selected = FightMode.FightBoxes.boxKey(self.box_selected, event.key)
                    
    def _setActionDisplay(self, text):
        self.action_display.appendleft( FightMode.shared['font_wrap'].renderInside(200, text, False, TEXT_COLOR) )
        self.action_set = not self.action_set
        
    def _playerActionDone(self):
        player_attack_defend = self.player_mon.fightHit(self.player_action)
        enemy_attack_defend = self.enemy_mon.fightHit(self.enemy_action)
        #print "player_attack_defend = " + str(player_attack_defend)
        #print "enemy_attack_defend  = " + str(enemy_attack_defend)
        damage_to_player = utility.reduceNumber(max( enemy_attack_defend[0] - player_attack_defend[1], 0))
        damage_to_enemy  = utility.reduceNumber(max(player_attack_defend[0] -  enemy_attack_defend[1], 0))
        if damage_to_player == 0 and damage_to_enemy == 0:
            damage_to_player = damage_to_enemy = 1
        #display results below
        self._setActionDisplay("Hit for " + str(damage_to_enemy) + "! Took " + str(damage_to_player) + "!")
        self.player_mon.stats['hpc'] -= damage_to_player
        self.enemy_mon.stats[ 'hpc'] -= damage_to_enemy
        
        if self.player_mon.stats['hpc'] < 1 and self.enemy_mon.stats['hpc'] < 1:
            self.player_action = 'draw'
        elif self.enemy_mon.stats['hpc'] < 1:
            self.player_action = 'win'
        elif self.player_mon.stats['hpc'] < 1:
            self.player_action = 'lose'
        else:
            self.player_action = False
        self.player_anim = 0
        self.enemy_action = False
        self.enemy_anim = 0
        
    def update(self):
        #enemy animation
        if self.enemy_action == 'attack':
            if self.enemy_anim == 0:
                self.enemy_rel[0] -= 1
                if self.enemy_rel[0] == -12:
                    self.enemy_anim = 1
            elif self.enemy_anim == 1:
                self.enemy_rel[0] += 1
                if self.enemy_rel[0] == 0:
                    self.enemy_anim = -1
        elif self.enemy_action == 'defend':
            if self.enemy_anim == 0:
                self.enemy_rel[0] += 1
                if self.enemy_rel[0] == 8:
                    self.enemy_anim = 1
            elif self.enemy_anim == 1:
                self.enemy_rel[0] -= 1
                if self.enemy_rel[0] == -4:
                    self.enemy_anim = 2
            elif self.enemy_anim == 2:
                self.enemy_rel[0] += 1
                if self.enemy_rel[0] == 0:
                    self.enemy_anim = -1
        #player animation, etc.
        if self.player_action == 'attack':
            if self.action_set == False:
                self._setActionDisplay("I'm gonna hit 'em!")
            if self.player_anim == 0:
                self.player_rel[0] += 1
                if self.player_rel[0] == 12:
                    self.player_anim = 1
            elif self.player_anim == 1:
                self.player_rel[0] -= 1
                if self.player_rel[0] == 0:
                    self.player_anim = -1
            else:
                self._playerActionDone()
        elif self.player_action == 'defend':
            if self.action_set == False:
                self._setActionDisplay("I'm gonna block 'em!")
            if self.player_anim == 0:
                self.player_rel[0] -= 1
                if self.player_rel[0] == -8:
                    self.player_anim = 1
            elif self.player_anim == 1:
                self.player_rel[0] += 1
                if self.player_rel[0] == 4:
                    self.player_anim = 2
            elif self.player_anim == 2:
                self.player_rel[0] -= 1
                if self.player_rel[0] == 0:
                    self.player_anim = -1
            else:
                self._playerActionDone()
        elif self.player_action == 'escape':
            if self.action_set == False:
                self._setActionDisplay("I'm gonna run away!")
            if self.player_anim == 0:
                self.player_rel[0] -= 1
                if self.player_rel[0] == -20:
                    self.player_anim = 1
            elif self.player_anim == 1:
                self.player_rel[0] += 5
                if self.player_rel[0] == 0:
                    self.player_anim = -1
            else:
                self._playerActionDone()
        elif self.player_action == 'draw':
            if self.player_anim == -1:
                return
            if self.player_anim < 6:
                self.player_anim += 1
            else:
                self.player_anim = -1
                self._setActionDisplay("They're both out cold.")
        elif self.player_action == 'win':
            if self.player_anim == -1:
                return
            if self.player_anim < 6:
                self.player_anim += 1
            else:
                self.player_anim = -1
                self._setActionDisplay("I won!!!")
        elif self.player_action == 'lose':
            if self.player_anim == -1:
                return
            if self.player_anim < 6:
                self.player_anim += 1
            else:
                self.player_anim = -1
                self._setActionDisplay(self.player_mon.name + "'s out cold.")
            
    def draw(self, screen):
        screen.fill(WHITE)
        screen.blit(FightMode.background, (0,0))
        if self.box_selected != FightMode.FightBoxes.elsewhere and self.action_set == False:
            screen.blit(FightMode.black_box, self.box_selected)
        #draw some mons and stuff
        self.player_mon.drawStanding(screen, (self.player_pos[0] + self.player_rel[0], self.player_pos[1] + self.player_rel[1]), True)
        self.enemy_mon.drawStanding( screen, (self.enemy_pos[0]  + self.enemy_rel[0] , self.enemy_pos[1]  + self.enemy_rel[1] ) )
        #draw health bar / health numbers / stats / etc
        for index, line in enumerate(self.action_display):
            screen.blit(line, (120, 166 - 10 * index))
        