import pygame as pg
from ..display.colours import *

class Bullet:
    """Your standard tank bullet"""

    def __init__(self, width, height, owner, DISPLAY_HEIGHT, DISPLAY_BASE):
        
        self.rotation = 0
        self.width = width
        self.height = height
        self.owner = owner