import pygame as pg
from ..display.colours import *

class PauseGui:
    """Pause menu screen"""
    def __init__(self, DISPLAY_BASE:int, DISPLAY_HEIGHT:int):
        self.surf = pg.Surface([DISPLAY_BASE, DISPLAY_HEIGHT])
        self.surf.set_colorkey(WHITE)
        self.surf.fill(WHITE)
        self.DISPLAY_BASE = DISPLAY_BASE
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT
        self.create_display()


    def create_display(self):
        pg.draw.rect(self.surf, PICKLE_GREEN, (self.DISPLAY_BASE/2-30, self.DISPLAY_HEIGHT/2-30, 60, 20),border_radius=10)


    