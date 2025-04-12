import pygame as pg
class Screen:
    """Class which contains all display-related functions, such as outputting"""
    def __init__(self, DISPLAY_BASE, DISPLAY_HEIGHT, GAME_BASE, GAME_HEIGHT):
        """Takes DISPLAY_BASE and DISPLAY_HEIGHT and uses them as width and height respectively for the Display"""
        self.DISPLAY= pg.display.set_mode((DISPLAY_BASE,DISPLAY_HEIGHT))
        self.GAME_BASE = GAME_BASE
        self.GAME_HEIGHT = GAME_HEIGHT
    
    def fill(self, colour):
        """Fills the screen with RGB value COLOUR"""
        self.DISPLAY.fill(colour)
    
    def render(self, bots, walls, player):
        ...
