import random
import os
import pygame

from constants import *
from skin import *
from feelings import *

random.seed()

class Monster(object):
    drv_max = 4
    lvl_max = 3
    main_stats = ('atk', 'def', 'spd', 'vit')
    sprite_path = os.path.join(GRAPHICS_DIRECTORY, MONSTER_PARTS_DIRECTORY)

    @classmethod
    def atLevel(cls, in_lvl, in_stats={}):
        """Create a new monster at a given level not above the maximum level, setting stats, etc. as needed."""
        new_mon = cls(in_stats)
        for n in range(min(in_lvl, cls.lvl_max)):
            new_mon.levelUp()
        return new_mon

    def __init__(self, in_stats={}):
        """Create a new monster, setting stats, etc. as needed."""
        self.sprite_size = (48,48)
        self.lvl = 0
        # self.awr might not even need to be a thing, remove this if it ends up not mattering
        self.awr = 0# awareness, this is a thing for conversations / progress through the game
        # it might make more sense to hold info for conversations flow in GameMode.shared, but I'm not sure
        # depends on how this number interacts with monster stuff
        self.personality = Personality.random()
        self.name = Personality.generateName(self.personality)
        self.skin = Skin.random(self.personality)
        # access the SkinTone with self.skin[self.lvl]
        self.mood = Mood.Neutral# mood might only be changed by and do stuff during battles / convos? maybe

        self.stats = {x: 2 for x in Monster.main_stats}
        self.stats['drv'] = Monster.drv_max//2
        self._levelStats()
        self.stats.update(in_stats)
        self.setHealth()

        self.sprite_groups = [random.choice(('A','B','C')) for x in range(5)]
        self.sprite =    pygame.image.load(os.path.join(Monster.sprite_path, '0-body-'+self.sprite_groups[1]+'.png'))
        self.sprite.blit(pygame.image.load(os.path.join(Monster.sprite_path, '0-head-'+self.sprite_groups[2]+'.png')), (0,0))
        self.sprite.blit(pygame.image.load(os.path.join(Monster.sprite_path, '0-legs-'+self.sprite_groups[3]+'.png')), (0,0))
        self._finishSprite()

    def fightStart(self):
        self.stats['drv'] = max(min(self.stats['drv'] + self.mood.drvChange, Monster.drv_max), 0)

    def _drvEffect(self):
        return self.stats['drv'] - Monster.drv_max + 1

    def fightHit(self, action):
        # todo: make speed affect more things
        attack = self.stats['atk']
        defend = self.stats['def']
        if action == 'attack':
            attack += self.stats['atk']//2 + self.stats['spd'] + random.randint(0,1)
            defend += self.stats['def']//2 + self.stats['atk']//2
        elif action == 'defend':
            attack += self.stats['atk']//2 + self.stats['def']//2
            defend += self.stats['atk']//2 + self.stats['spd'] + random.randint(0,1)
        else:# 'escape'
            attack = attack//2 + self.stats['spd']//2
            defend = defend//2 + self.stats['spd']//2
        attack = max(attack + random.randint(-1,1) + self._drvEffect(), 0)
        defend = max(defend + random.randint(-1,1) + self._drvEffect(), 0)
        return (attack, defend)

    def _finishSprite(self):
        # self.sprite_size = (64,64)
        # self.sprite = pygame.Surface((64,64))
        # self.sprite.fill((255,0,0))
        self.sprite = self.sprite.convert_alpha()
        self.sprite_right = pygame.transform.flip(self.sprite, True, False)

    def _levelStats(self):
        for stat in Monster.main_stats:
            self.stats[stat] += 2
        for stat in random.sample(Monster.main_stats, 2):
            self.stats[stat] += 1
        self.stats[self.personality.stat] += 2

    def setHealth(self):
        self.stats['hpm'] = self.stats['vit']*2 + self.stats['vit']//2 + self.stats['vit']//4
        self.stats['hpc'] = self.stats['hpm']

    def darkSkin(self):
        return self.skin[self.lvl].dark

    def lightSkin(self):
        return self.skin[self.lvl].light

    def levelUp(self):
        """Level up a monster, setting stats, etc. as needed."""
        if self.lvl >= Monster.lvl_max:
            return 0
        self.lvl += 1
        if self.lvl > 2:
            self.sprite_size = (64,64)
        self._levelStats()
        self.setHealth()
        # find sprite paths
        tailPath = os.path.join(Monster.sprite_path, str(self.lvl)+'-tail-'+self.sprite_groups[0]+str(random.randint(0,2))+'.png')
        bodyPath = os.path.join(Monster.sprite_path, str(self.lvl)+'-body-'+self.sprite_groups[1]+str(random.randint(0,2))+'.png')
        headPath = os.path.join(Monster.sprite_path, str(self.lvl)+'-head-'+self.sprite_groups[2]+str(random.randint(0,2))+'.png')
        legsPath = os.path.join(Monster.sprite_path, str(self.lvl)+'-legs-'+self.sprite_groups[3]+str(random.randint(0,2))+'.png')
        armsPath = os.path.join(Monster.sprite_path, str(self.lvl)+'-arms-'+self.sprite_groups[4]+str(random.randint(0,2))+'.png')
        # sprite construction stuff
        self.sprite = pygame.image.load(tailPath)
        self.sprite.blit(pygame.image.load(bodyPath), (0,0))
        self.sprite.blit(pygame.image.load(headPath), (0,0))
        self.sprite.blit(pygame.image.load(legsPath), (0,0))
        self.sprite.blit(pygame.image.load(armsPath), (0,0))
        # color swapping stuff
        pix_array = pygame.PixelArray(self.sprite)
        pix_array.replace(self.skin[0].dark, self.darkSkin())
        pix_array.replace(self.skin[0].light, self.lightSkin())
        del pix_array
        self._finishSprite()
        print("Level up: " + self.name)
        print("tailPath: " + tailPath)
        print("bodyPath: " + bodyPath)
        print("headPath: " + headPath)
        print("legsPath: " + legsPath)
        print("armsPath: " + armsPath)
        return 1

    def drawCentered(self, screen, pos, right=False):
        """Draw the monster on the screen, with its center at the position passed."""
        self.draw(screen, (pos[0]-self.sprite_size[0]//2, pos[1]-self.sprite_size[1]//2), right)

    def drawStanding(self, screen, pos, right=False):
        """Draw the monster on the screen, with its bottom-center at the position passed."""
        self.draw(screen, (pos[0]-self.sprite_size[0]//2, pos[1]-self.sprite_size[1]), right)

    def draw(self, screen, pos, right=False):
        """Draw the monster on the screen."""
        screen.blit(self.sprite if not right else self.sprite_right, pos)
