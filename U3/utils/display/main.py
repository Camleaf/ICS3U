import pygame as pg
from ..player.main import Player
from ..walls.main import Walls
from ..enemies.main import Enemies
from .colours import *
from .background import Background
class Screen:
    """Class which contains all display-related functions, such as outputting"""
    def __init__(self, DISPLAY_BASE, DISPLAY_HEIGHT, GAME_BASE, GAME_HEIGHT):
        """Takes DISPLAY_BASE and DISPLAY_HEIGHT and uses them as width and height respectively for the Display"""
        self.DISPLAY= pg.display.set_mode((DISPLAY_BASE,DISPLAY_HEIGHT))
        self.DISPLAY_BASE = DISPLAY_BASE
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT
        self.GAME_BASE = GAME_BASE
        self.GAME_HEIGHT = GAME_HEIGHT

        self.background = Background(GAME_BASE,GAME_HEIGHT,DISPLAY_BASE, DISPLAY_HEIGHT)
    
    def fill(self, colour):
        """Fills the screen with RGB value COLOUR"""
        self.DISPLAY.fill(colour)
    
    def render(self, player:Player, player_container, walls:Walls, enemies:Enemies):
        """Wrapper function to render all objects to the display. Requires the barrier, the walls group, the player container, and the enemies group as input"""
        


        # local render systems
        # reserved for objects which have their own render functions, such as barriers
        self.background.Render(self.DISPLAY, player.camera_x, player.camera_y)
        walls.render(self.DISPLAY, player.camera_x, player.camera_y)
        enemies.render(self.DISPLAY,player.camera_x, player.camera_y)
        #barrier.render(self.DISPLAY, player.camera_x, player.camera_y, self.DISPLAY_BASE, self.DISPLAY_HEIGHT)
        
        
        # no render systems
        # reserved for objects without a local render system such as the player class
        player_container.draw(self.DISPLAY)

    def blit(self, object):
        """Shorthand for pygame surface.blit function"""
        self.DISPLAY.blit(object)
    