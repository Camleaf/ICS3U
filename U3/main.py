### Tanks game

# library imports
import sys,time,threading, pygame as pg
from lib.pymenu import pymenu as mu
from pygame.locals import *

# local imports
from utils.display.colours import *

from utils.menu.main import Menu
from utils.container.container import Container

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

c = Container(DISPLAY_BASE, DISPLAY_HEIGHT, GAME_BASE, GAME_HEIGHT)
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
            if keys_pressed[pg.K_SPACE]:
                
                if player_shot_cooldown > 20:
                    player_shot_cooldown = 0
                    c.player.fire()
        
        

                

    if not c.interrupt_menu_active and not c.game_end:
        c.player.move(x_vector,y_vector, c.enemies.units)
        c.enemies.check_shots(tick)
        c.player.magazine.update_bullets(c.enemies,c.player, menu)
        c.enemies.move(c.player, menu)
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