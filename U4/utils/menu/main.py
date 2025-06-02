import pygame as pg
from typing import Any
from ..display.colours import *
from lib.pymenu import pymenu as mu
from .frames import create_frames
import os

class Menu:
    """Menu container which uses Pymenu to create a dynamic menu screen"""
    def __init__(self, DISPLAY_BASE:int,DISPLAY_HEIGHT:int, container):
        self.window = mu.Window(DISPLAY_BASE, DISPLAY_HEIGHT)
        self.window.set_font_file(os.path.join(f'{os.getcwd()}','assets','gameFont.ttf'))
        self.window.set_placeholder_file(os.path.join(f'{os.getcwd()}','assets','Placeholder.png'))



        self.c = container
        create_frames(self.window, DISPLAY_BASE,DISPLAY_HEIGHT)

        self.current_frame = 'welcome'

        self.window.load_frame("welcome")

    def switch_frame(self,target_frame):
        """Calls pymenu.window function load_frame, and sets current frame to the target frame"""
        self.window.load_frame(target_frame)
        self.current_frame = target_frame
        return False

    def render(self, DISPLAY: pg.Surface):
        """Renders self.surface to a given display at (0,0)"""
        DISPLAY.blit(self.surface())

    def surface(self):
        """Returns the current window surface"""
        return self.window.surface()