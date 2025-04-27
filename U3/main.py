### Tanks game

# library imports
import sys,time,threading, pygame as pg
from lib.pymenu import pymenu as mu
from pygame.locals import *

# local imports
from utils.display.main import Screen
from utils.display.colours import *

from utils.player.main import Player, Create_Container
from utils.walls.main import Walls
from utils.enemies.main import Enemies
from utils.menu.main import Menu

# variables
DISPLAY_BASE = 700
DISPLAY_HEIGHT = 700
GAME_BASE = 1190
GAME_HEIGHT = 1190

# init pygame
pg.init()
clock = pg.time.Clock()
# functions for menu



# classes
class Container:
    """Acts as a container which keep state between game objects when they are passed between files"""

    def __init__(self):
        self.max_difficulty = 7

        self.diff_word = {
            1:"civilian",
            2:"cadet",
            3:"ensign",
            4:"captain",
            5:"commodore",
            6:"admiral",
            7:"grand admiral",
        }


        self.refresh_state()

    def refresh_state(self):
        """Used for initalizing a game state, such as on game start or when going to main menu"""
        
        self.game_end = False
        self.interrupt_menu_active = True
        self.difficulty = 1
        self.screen = Screen(DISPLAY_BASE,DISPLAY_HEIGHT, GAME_BASE, GAME_HEIGHT)
        self.walls = Walls(GAME_BASE,GAME_HEIGHT, DISPLAY_BASE, DISPLAY_HEIGHT)
        self.player = Player(40,40,DISPLAY_BASE, DISPLAY_HEIGHT, GAME_BASE, GAME_HEIGHT)
        self.player_container = Create_Container(self.player)
        self.enemies = Enemies(5,40,40,GAME_BASE, GAME_HEIGHT,DISPLAY_BASE, DISPLAY_HEIGHT, self.walls, self.player.camera_x, self.player.camera_y, 5)
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

    def end_game(self):
        self.game_end = True
        self.interrupt_menu_active = True
        self.player.is_alive = False
        time.sleep(0.1)

c = Container()
menu = Menu(GAME_BASE, GAME_HEIGHT, c)

# Threads


# define the camera. will continuosly update as a result of inheritance from player

camera_x = c.player.camera_x
camera_y = c.player.camera_y

# mainloop
frames_num = 1
tick = 0
player_shot_cooldown = 0
menu_input_timer = 0

while True:

    for event in pg.event.get():
        if event.type == QUIT:
            c.player.is_alive = False
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if c.interrupt_menu_active:
                menu.window.mouseInteraction(pg.mouse.get_pos())
        # If i end up needing text I'll add it then
        if event.type == pg.KEYDOWN:
            
            key = event.dict['unicode']
            if not c.game_end:
                if key in ('\x1b'):
                    if menu.current_frame == "pause":
                        menu.switch_frame('ingame')
                        c.time_control(False)
                    elif menu.current_frame == 'ingame':
                        menu.switch_frame('pause')
                        c.time_control(True)




    c.screen.fill(BLACK)

    if keys_pressed := pg.key.get_pressed():


        x_vector = 0
        y_vector = 0
        if not c.interrupt_menu_active and not c.game_end:
            if keys_pressed[pg.K_a]:
                x_vector -= 2.5
                
            if keys_pressed[pg.K_d]:
                x_vector += 2.5
            if keys_pressed[pg.K_w]:
                y_vector -= 2.5
            if keys_pressed[pg.K_s]:
                y_vector += 2.5
            if keys_pressed[pg.K_q]:
                time.sleep(10)
            if keys_pressed[pg.K_SPACE]:
                
                if player_shot_cooldown > 20:
                    player_shot_cooldown = 0
                    c.player.fire()
        
        

                

    if not c.interrupt_menu_active and not c.game_end:
        c.player.move(x_vector,y_vector, c.enemies.units)
        c.enemies.check_shots(tick)
        c.player.magazine.update_bullets(c.enemies,c.player)
        c.enemies.move(c.player)
    # run all the time
    c.screen.render(c.player, c.player_container, c.walls, c.enemies, menu)
    if not c.game_end:
        if not c.player.is_alive: 
            c.game_end = True
            menu.end_game(False)
        elif len(c.enemies.units) == 0:
            c.game_end = True
            menu.end_game(True)


    pg.display.flip()
    

    player_shot_cooldown += 1
    if tick == 0:
        print(f"{frames_num} second")
        frames_num += 1
    tick += 1
    tick %= 60
    if menu_input_timer < 11:
        menu_input_timer += 1
    clock.tick(60)