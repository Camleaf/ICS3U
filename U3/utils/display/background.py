import pygame as pg
import os
class Background:
    def __init__(self, GAME_BASE, GAME_HEIGHT,DISPLAY_BASE, DISPLAY_HEIGHT):
        """Container for the tiled repeating background"""
        self.GAME_BASE = GAME_BASE
        self.GAME_HEIGHT = GAME_HEIGHT
        self.DISPLAY_BASE = DISPLAY_BASE
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT
        self.Create_Surface()

    def Create_Surface(self):
        """Creates the surface used by the display"""
        self.tile = pg.transform.scale(pg.image.load(os.path.join('assets','tileable.jpg')), (100,100))
        self.surface = pg.Surface([self.GAME_BASE, self.GAME_HEIGHT])
        for x in range(0,self.GAME_BASE,100):
            for y in range(0,self.GAME_HEIGHT,100):
                self.surface.blit(self.tile, (x,y))
        self.surface = self.surface.convert()

    def Render(self, DISPLAY, camera_x, camera_y):
        DISPLAY.blit(self.surface, (-camera_x+self.DISPLAY_BASE/2, -camera_y+self.DISPLAY_HEIGHT/2))