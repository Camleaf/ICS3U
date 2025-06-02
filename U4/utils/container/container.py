
# library imports
import time,threading, pygame as pg
from pygame.locals import *

# local imports
from utils.display.main import Screen
from utils.display.colours import *

class Container:
    """Acts as a container which keep state between game objects when they are passed between files"""
    screen:Screen

    
    def __init__(self, DISPLAY_BASE, DISPLAY_HEIGHT):
        self.DISPLAY_BASE = DISPLAY_BASE
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT

        self.refresh_state()

    def refresh_state(self):
        """Used for initalizing a game state, such as on game start or when going to main menu"""
        self.screen = Screen(self.DISPLAY_BASE, self.DISPLAY_HEIGHT)

    def end_game(self,win=False):
        """Ends the game, checks if from menu or from death/win and updates accordingly"""
        ...