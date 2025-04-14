import pygame as pg
from ..display.colours import *


class Enemy:
    """The individual class for each enemy"""
    def __init__(self, color, width, height, posx, posy, DISPLAY_HEIGHT, DISPLAY_BASE, GAME_BASE, GAME_HEIGHT):
        self.image_orig = pg.Surface([width,height])
        self.image_orig.set_colorkey((255,255,255))
        self.image_orig.fill(color)
        pg.draw.rect(self.image_orig,OFF_YELLOW,(0,height-height/9,width,height/9))
        pg.draw.rect(self.image_orig,OFF_YELLOW,(width/9,0,width/7,height))
        pg.draw.rect(self.image_orig,OFF_YELLOW,(width-width/9-width/7,0,width/7,height))


        self.x = posx
        self.y = posy

        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.center = [posx-DISPLAY_BASE//2+GAME_BASE//2, posy-DISPLAY_HEIGHT//2+GAME_HEIGHT//2] # this is just initial we change it later
    
