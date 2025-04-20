import pygame as pg
from ..display import colours

class Menu:
    """The container for all instances of the menu"""

    def __init__(self, DISPLAY_BASE:int, DISPLAY_HEIGHT:int):

        self.DISPLAY_BASE = DISPLAY_BASE
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT

        # there will be four menus. One for endscreen, one for start screen, one for pause, and one for during play