import pygame as pg
from ..display.colours import *

class Bullet:
    """Your standard tank bullet"""

    def __init__(self, width, height, owner, speed, angle, start, targets, walls):
        
        self.rotation = 0
        self.width = width
        self.height = height
        self.owner = owner
        self.walls = walls
        self.speed = speed
        self.angle = angle
        self.x, self.y = start
        


        
    
    def move(self):
        ...
