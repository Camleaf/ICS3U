import time
import pygame as pg
from typing import Any
from ..display.colours import *
from lib.pymenu import pymenu as mu
from .frames import create_frames
import os


class Menu:
    """Menu container which uses Pymenu to create a dynamic menu screen"""
    def __init__(self, GAME_BASE, GAME_HEIGHT):

        self.window = mu.Window(GAME_BASE,GAME_HEIGHT, OFF_GREY)
        self.window.set_font_file(os.path.join(f'{os.getcwd()}','lib','pymenu','gameFont.ttf'))
        create_frames(self.window)


        self.window.load_frame("start")


    def render(self, DISPLAY: pg.Surface):
        DISPLAY.blit(self.surface())

    def surface(self):
        return self.window.surface()