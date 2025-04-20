import time
import pygame as pg
from typing import Any
from ..display.colours import *
from .startgui import StartGui
from .pausegui import PauseGui
from .gamegui import GameGui

class Menu:
    """The container for all instances of the menu"""

    def __init__(self, DISPLAY_BASE:int, DISPLAY_HEIGHT:int):

        self.DISPLAY_BASE = DISPLAY_BASE
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT

        # there will be four menus. One for endscreen, one for start screen, one for pause, and one for during play

        self.menu_list: dict[str,Any] = { # add more as I go
            "start": StartGui(DISPLAY_BASE, DISPLAY_HEIGHT), # working on pausegui atm
            "pause": PauseGui(DISPLAY_BASE, DISPLAY_HEIGHT),
            "ingame": GameGui(DISPLAY_BASE, DISPLAY_HEIGHT)
        }
        self.switch_gui("ingame")

    def switch_gui(self, version):
        self.surf = pg.Surface([self.DISPLAY_BASE, self.DISPLAY_HEIGHT])
        self.surf.set_colorkey(WHITE)
        self.surf.fill(WHITE)
        self.surf.blit(self.menu_list[version].surf,(0,0))
        time.sleep(0.2)
    
    def render(self, DISPLAY:pg.Surface):
        DISPLAY.blit(self.surf,(0,0))