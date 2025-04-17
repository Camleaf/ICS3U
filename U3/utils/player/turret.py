import pygame as pg
from ..display.colours import *

class Turret:
    """The turret animation for the player"""

    def __init__(self, width, height, DISPLAY_HEIGHT, DISPLAY_BASE):
        
        self.rotation = 0
        self.width = width
        self.height = height
        self.image_orig = pg.Surface([width,height])
        self.image_orig.set_colorkey((255,255,255))
        self.image_orig.fill(BLACK)
        self.image = self.image_orig.copy()
        