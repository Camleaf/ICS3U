import pygame as pg
from ..display.colours import *
import math

class Bullet:
    """Your standard tank bullet"""

    def __init__(self, width, height, owner, speed, angle, start, grid):
        
        self.rotation = 0
        self.width = width
        self.height = height
        self.owner = owner
        self.speed = speed
        self.angle = angle
        self.grid = grid
        self.x, self.y = start
        self.image = pg.Surface([width,height])
        self.image.set_colorkey((255,255,255))
        self.image.fill(WHITE)
        pg.draw.circle(self.image, OFF_BLACK, (self.width/2, self.height/2),radius=4)

        vector = pg.math.Vector2((0,1))
        vector = vector.rotate(-angle+180)
        self.xspeed = speed * vector[0]
        self.yspeed = speed * vector[1]
        self.traveled = 0
        self.max_dist = 300 if self.owner == "player" else 350 # bots have longer range than players to force close engagement
        # add a medium significance random distance for the bullet max distance so that it isn't as easy for the player to use the
        # disappearance to their advantage


        
    
    def move(self, targets, enemies, player):
        self.x += self.xspeed
        self.y += self.yspeed
        self.traveled += self.speed
        if self.collision(targets, enemies, player):
            return True
        elif self.traveled > self.max_dist:
            return True
        else:
            return False
        
        

    def collision(self,targets, enemies, player):

        if self.y < 0 or (len(self.grid))*70 <= self.y or self.x < 0 or (len(self.grid[0]))*70 <=self.x: 
            return True
        if self.grid[int((self.y)//70)][int((self.x)//70)] == 1:
            self.hit(enemies, player,playerhit=False, bot=False, bot_index=None)
            return True
        if self.owner == "player":
            for i,unit in enumerate(targets):
                n_x = unit.x  + unit.offset
                n_y = unit.y + unit.offset
          #print(unit.y, unit.x)

                collider = pg.Rect(n_x,n_y, unit.width, unit.height)
                if collider.collidepoint(self.x, self.y):
                    self.hit( enemies, player,playerhit=False, bot=True, bot_index=unit.id)
                    return True
        else:
            n_x, n_y = targets[0]
            collider = pg.Rect(n_x,n_y, 40, 40)
            if collider.collidepoint(self.x, self.y):
                self.hit(enemies, player,playerhit=True, bot=False, bot_index=None)
                return True
        


        return False
    

    def hit(self, enemies, player, playerhit=False, bot=False, bot_index=None):
        if playerhit:
            player.game_over()
            
        elif bot:
            enemies.destroy_unit(bot_index)
        
