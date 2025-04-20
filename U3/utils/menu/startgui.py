import pygame as pg
from ..display.colours import *

class StartGui:
    """Start"""
    def __init__(self, DISPLAY_BASE:int, DISPLAY_HEIGHT:int):
        self.surf = pg.Surface([DISPLAY_BASE, DISPLAY_HEIGHT])
        self.surf.set_colorkey(WHITE)
        self.surf.fill(WHITE)
        self.DISPLAY_BASE = DISPLAY_BASE
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT
        self.create_display()


    def create_display(self):
        ...


    