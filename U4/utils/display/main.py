import pygame as pg
from .colours import *

class Screen:
    """Class which contains all display-related functions, such as outputting"""
    def __init__(self, DISPLAY_BASE, DISPLAY_HEIGHT):
        """Takes DISPLAY_BASE and DISPLAY_HEIGHT and uses them as width and height respectively for the Display"""
        self.DISPLAY= pg.display.set_mode((DISPLAY_BASE,DISPLAY_HEIGHT),pg.SRCALPHA)
        self.DISPLAY_BASE = DISPLAY_BASE
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT
    
    def fill(self, colour):
        """Fills the screen with RGB value COLOUR"""
        self.DISPLAY.fill(colour)
    
    def render(self, *provided):
        """Wrapper function to render all provided objects to the display. """
        
        for item in provided:
            item.render(self.DISPLAY)

        
        

    def blit(self, object):
        """Shorthand for pygame surface.blit function"""
        self.DISPLAY.blit(object)
    