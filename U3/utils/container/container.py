
# library imports
import time,threading, pygame as pg
from pygame.locals import *

# local imports
from utils.display.main import Screen
from utils.display.colours import *

from utils.player.main import Player, Create_Container
from utils.walls.main import Walls
from utils.enemies.main import Enemies

class Container:
    """Acts as a container which keep state between game objects when they are passed between files"""
    diff_word = {
            1:"civilian",
            2:"cadet",
            3:"enlist",
            4:"corporal",
            5:"sergeant",
            6:"officer",
            7:"general",
        }
    def __init__(self, DISPLAY_BASE, DISPLAY_HEIGHT, GAME_BASE, GAME_HEIGHT):
        self.DISPLAY_BASE = DISPLAY_BASE
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT
        self.GAME_BASE = GAME_BASE
        self.GAME_HEIGHT = GAME_HEIGHT
        self.max_difficulty = 7
        self.gold = 0
        self.raw_gain = 0
        self.repair = 0
        self.gold_gain = 0
        self.difficulty = 1
        self.lives = 1
        self.player_bullet_dist_mult = 1
        self.player_speed_mult = 1
        self.refresh_state()
        self.interrupt_menu_active = True

    def refresh_state(self):
        """Used for initalizing a game state, such as on game start or when going to main menu"""
        self.gold_gain = 0
        self.raw_gain = 0
        self.repair = 0
        self.game_end = False
        self.interrupt_menu_active = False
        self.screen = Screen(self.DISPLAY_BASE,self.DISPLAY_HEIGHT, self.GAME_BASE, self.GAME_HEIGHT)
        self.walls = Walls(self.GAME_BASE,self.GAME_HEIGHT, self.DISPLAY_BASE, self.DISPLAY_HEIGHT)
        self.player = Player(40,40,self.DISPLAY_BASE, self.DISPLAY_HEIGHT, self.GAME_BASE, self.GAME_HEIGHT,self.player_bullet_dist_mult,self.player_speed_mult,lives=self.lives)
        self.player_container = Create_Container(self.player)
        self.enemies = Enemies(40,40,self.GAME_BASE, self.GAME_HEIGHT, self.DISPLAY_BASE, self.DISPLAY_HEIGHT, self.walls, self.player.camera_x, self.player.camera_y, self.difficulty, 100)
        self.player.create_magazine(self.walls)
        self.in_range_walls = threading.Thread(target = self.player.get_in_range_walls, args = (self.walls,))
        self.in_range_walls.daemon = True
        self.in_range_walls.start()

    def time_control(self, on_off:bool):
        """Used for pausing and unpausing the game"""
        if on_off:
            self.interrupt_menu_active = True
        else:
            self.interrupt_menu_active = False

    def end_game(self,win=False):
        """Ends the game, checks if from menu or from death/win and updates accordingly"""
        self.game_end = True
        self.gold_gain = 0
        if not self.interrupt_menu_active:
            raw = self.enemies.end_game()
            self.raw_gain = raw['increase']
            self.repair = raw['repair_cost'] # the repair cost is proportional to the difficulty of the mission. High risk high reward. See end_Game function in enemies/main.py
            if win:
                self.gold_gain = self.raw_gain
                self.repair = 0
            else:
                self.gold_gain = self.raw_gain - self.repair
            
            self.gold += self.gold_gain
            if self.gold < 0:
                self.gold = 0
        
        self.interrupt_menu_active = True
        self.player.is_alive = False
        time.sleep(0.1)