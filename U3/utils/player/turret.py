import pygame as pg
from ..display.colours import *
import math

class Turret(pg.sprite.Sprite):
    """The turret animation for the player"""

    def __init__(self, width, height, DISPLAY_HEIGHT, DISPLAY_BASE):
        pg.sprite.Sprite.__init__(self)
        self.rotation = 0
        self.fwidth = width
        self.fheight = height
        self.image_orig = pg.Surface([width,height])
        self.image_orig.set_colorkey(BLACK)
        self.image_orig.fill(BLACK)
        pg.draw.rect(self.image_orig, OFF_BLACK, (self.fwidth/2-5,self.fheight/2-5,10,10),border_radius=4)
        pg.draw.rect(self.image_orig, OFF_BLACK, (self.fwidth/2-5,self.fheight/2-30,10,30),border_radius=2)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (DISPLAY_BASE/2, DISPLAY_HEIGHT/2)
        self.raw_x, self.raw_y = 0,0
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT
        self.DISPLAY_BASE = DISPLAY_BASE


    def rotation_manager(self):
        self.raw_x, self.raw_y = pg.mouse.get_pos()
        relative_x, relative_y = self.raw_x - self.DISPLAY_BASE // 2, self.raw_y - self.DISPLAY_HEIGHT//2

        angle = math.degrees(math.atan2(relative_y,relative_x))
        self.rotation = -angle -90
        #print(relative_x,relative_y,angle)
        self.rotate()


    def rotate(self):
        """Rotates the turret image to rotation"""
        old_centre = self.rect.center
        self.image = pg.transform.rotate(self.image_orig, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = old_centre  