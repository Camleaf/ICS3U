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
        self.c = container
        create_frames(self.window,self, GAME_BASE,GAME_HEIGHT)

        self.current_frame = 'welcome'

        self.window.load_frame("welcome")

    def switch_frame(self,target_frame):
        """Calls pymenu.window function load_frame, and sets current frame to the target frame"""
        self.window.load_frame(target_frame)
        self.current_frame = target_frame
        self.update_gold_count()
        return False
    
    def menu_exit(self):
        """Shorthand for switching to the main menu and refreshing all the variables"""
        self.c.end_game()
        return self.switch_frame('main')
        
    def resume_game(self):
        self.c.time_control(False)
        self.switch_frame("ingame")
        return False
    
    def enter_game(self):
        """Shorthand for removing the menu and unpausing the game"""
        self.c.time_control(False)
        self.switch_frame("ingame")
        self.c.refresh_state()
        self.update_lives()
        return False
    
    def update_lives(self):
        for life in range(self.c.player.max_lives):
            if life >= self.c.player.lives:
                self.window.update_stat("Life"+str(life), image_path=os.path.join(f"{os.getcwd()}","assets","Transparent.png"))
            else:
                self.window.update_stat("Life"+str(life), image_path=os.path.join(f"{os.getcwd()}","assets","images","Heart.png"))
            self.window.update_surf("Life"+str(life), False)

    def end_game(self, win):
        """Changes the text on the winscreen during the end game"""
        self.c.end_game(win)
        self.switch_frame('endgame')
        if win:
            self.update_text('VICTORY', 'StatusLabel',(0,0,0,100))
            self.update_text('Destroying those tanks sure brings a reward...',"DescrText", update_bg=False)
            
        else:
            self.update_text('DEFEAT', 'StatusLabel',(0,0,0,100))
            self.update_text('Getting repairs cost you; Try not to do that...',"DescrText", update_bg=False)
            
        if self.c.gold_gain < 0:
            self.update_text("You lost", ID='GoldGainedText',update_bg=False)
        else:
            self.update_text("You gained", ID='GoldGainedText',update_bg=False)
        self.update_text(str(abs(self.c.gold_gain)), ID='GoldGained',update_bg=False)
        self.update_text(f"Gain: {self.c.raw_gain}", ID="RawGain", update_bg=False)
        self.update_text(f"Repair: {self.c.repair}", ID="RawRepair", update_bg=False)

    def update_text(self, text:str, ID:str,bg_color:tuple[int]=(0,0,0,0), update_bg:bool=True):
        """Updates the text of the given ID, can choose to update the background"""
        self.window.update_stat(ID, text=text)
        self.window.update_surf(ID, bg_color, update_bg)

    def upgrade(self, up_type:str):

        cost = int(self.window.return_state(up_type+"Cost").text)
        level = int(self.window.return_state(up_type+"LevelNum").text)
        
        if cost > self.c.gold:
            return False

        if up_type == "Health" and self.c.lives+1 <= self.c.player.max_lives:
            self.c.lives += 1
        elif up_type == "Distance":
            self.c.player_bullet_dist_mult += 0.1
        elif up_type == "Speed":
            self.c.player_speed_mult += 0.1
        self.update_text(ID=up_type+"Cost", text=str(cost*2), update_bg=False)
        self.update_text(ID=up_type+"LevelNum", text=str(level+1), update_bg=False)
        self.c.gold -= cost
        self.update_gold_count()
        # actually add upgrade
        return False
        

    def set_difficulty(self, increment:bool=False):
        """Sets the difficulty with a min of 1 and a max of 7. Can increment or decrement"""
        if increment:
            self.c.difficulty += 1

        else:
            self.c.difficulty -= 1

        if self.c.difficulty < 1:
            self.c.difficulty = 1
        elif self.c.difficulty > 7:
            self.c.difficulty = 7
        
        self.update_text(self.c.diff_word[self.c.difficulty].title(),'DifficultyText',update_bg=False)
        return False
    
    def update_gold_count(self): #gold count id will always be GoldNum
        """Updates the text on screen with ID \'GoldNum\' to match the current number count if it exists"""
        if 'GoldNum' in self.window._objects:
            self.update_text(str(self.c.gold), ID='GoldNum',update_bg=False)
        if 'GoldGain' in self.window._objects:
            self.update_text(str(abs(self.c.gold_gain)), ID='GoldGain', update_bg=False)

    def render(self, DISPLAY: pg.Surface):
        DISPLAY.blit(self.surface())

    def surface(self):
        """Returns the current window surface"""
        return self.window.surface()