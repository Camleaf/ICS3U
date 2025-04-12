import pygame as pg
class Display:
    """Class which contains all display-related functions, such as outputting"""
    def __init__(self, DISPLAY_BASE, DISPLAY_HEIGHT):
        """Takes DISPLAY_BASE and DISPLAY_HEIGHT and uses them as width and height respectively for the Display"""
        self.DISPLAY= pg.display.set_mode((DISPLAY_BASE,DISPLAY_HEIGHT))
    
    def fill(self, colour):
        """Fills the screen with RGB value COLOUR"""
        self.DISPLAY.fill(colour)