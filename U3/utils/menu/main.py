import time
import pygame as pg
from typing import Any
from ..display.colours import *
from lib.pymenu import pymenu as mu
from .frames import create_frames
import os


class Menu:
    """Menu container which uses Pymenu to create a dynamic menu screen"""
    def __init__(self, GAME_BASE, GAME_HEIGHT, pause_control):

        self.window = mu.Window(GAME_BASE,GAME_HEIGHT, OFF_GREY)
        self.window.set_font_file(os.path.join(f'{os.getcwd()}','assets','gameFont.ttf'))
        create_frames(self.window,self, GAME_BASE,GAME_HEIGHT)
        self.pause_control = pause_control

        self.window.load_frame("welcome")

    def switch_frame(self,target_frame):
        
        self.window.load_frame(target_frame)
        return False
    
    def enter_game(self):
        self.pause_control.time_control(False)
        self.switch_frame("ingame")
        return False

    def render(self, DISPLAY: pg.Surface):
        DISPLAY.blit(self.surface())

    def surface(self):
        return self.window.surface()