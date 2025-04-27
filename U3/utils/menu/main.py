import time
import pygame as pg
from typing import Any
from ..display.colours import *
from lib.pymenu import pymenu as mu
from .frames import create_frames
import os


class Menu:
    """Menu container which uses Pymenu to create a dynamic menu screen"""
    def __init__(self, GAME_BASE, GAME_HEIGHT, container):

        self.window = mu.Window(GAME_BASE,GAME_HEIGHT, OFF_GREY)
        
        self.window.set_font_file(os.path.join(f'{os.getcwd()}','assets','gameFont.ttf'))
        self.window.set_placeholder_file(os.path.join(f'{os.getcwd()}','assets','Placeholder.png'))
        create_frames(self.window,self, GAME_BASE,GAME_HEIGHT)
        self.c = container

        self.current_frame = 'welcome'

        self.window.load_frame("welcome")

    def switch_frame(self,target_frame):
        
        self.window.load_frame(target_frame)
        self.current_frame = target_frame
        return False
    
    def restart_game(self):
        self.c.refresh_state()
        return self.switch_frame('main')
        


    def enter_game(self):
        self.c.time_control(False)
        self.switch_frame("ingame")
        return False

    def end_game(self, win):
        self.c.end_game()
        self.switch_frame('endgame')
        if win:
            self.update_text('You Win!!!!', 'StatusLabel',(0,0,0,100))
        else:
            self.update_text('You Lost...', 'StatusLabel',(0,0,0,100))

    def update_text(self, text:str, ID:str,bg_color:tuple[int]=(0,0,0,0), update_bg:bool=True):
        self.window.update_stat(ID, text=text)
        self.window.update_surf(ID, bg_color, update_bg)


    def set_difficulty(self, increment:bool=False):
        if increment:
            self.c.difficulty += 1

        else:
            self.c.difficulty -= 1

        if self.c.difficulty < 1:
            self.c.difficulty = 7
        elif self.c.difficulty > 7:
            self.c.difficulty = 1
        
        self.update_text(self.c.diff_word[self.c.difficulty].title(),'DifficultyText',update_bg=False)


    def render(self, DISPLAY: pg.Surface):
        DISPLAY.blit(self.surface())

    def surface(self):
        return self.window.surface()