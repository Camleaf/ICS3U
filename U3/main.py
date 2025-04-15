### Tanks game

# system imports
import sys,time,threading, pygame as pg
from pygame.locals import *

# local imports
from utils.display.main import Screen
from utils.display.colours import *

from utils.player.main import Player, Create_Container
from utils.walls.main import Walls
from utils.enemies.main import Enemies

# variables
DISPLAY_BASE = 700
DISPLAY_HEIGHT = 700
GAME_BASE = 1190
GAME_HEIGHT = 1190


# classes
screen = Screen(DISPLAY_BASE,DISPLAY_HEIGHT, GAME_BASE, GAME_HEIGHT)
clock = pg.time.Clock()

walls = Walls(GAME_BASE,GAME_HEIGHT, DISPLAY_BASE, DISPLAY_HEIGHT)
player = Player(PICKLE_GREEN,40,40,DISPLAY_BASE, DISPLAY_HEIGHT, GAME_BASE, GAME_HEIGHT)
player_container = Create_Container(player)
enemies = Enemies(1,40,40,DISPLAY_BASE, DISPLAY_HEIGHT, GAME_BASE, GAME_HEIGHT, walls, player.camera_x, player.camera_y)


# Threads
in_range_walls = threading.Thread(target = player.get_in_range_walls, args = (walls,))
in_range_walls.start()

# define the camera. will continuosly update as a result of inheritance from player

camera_x = player.camera_x
camera_y = player.camera_y


# mainloop
while True:
    
    for event in pg.event.get():
        if event.type == QUIT:
            player.is_alive = False
            pg.quit()
            sys.exit()

    screen.fill(BLACK)

    if keys_pressed := pg.key.get_pressed():
        x_vector = 0
        y_vector = 0
        if keys_pressed[pg.K_LEFT]:
            x_vector -= 2
            
        if keys_pressed[pg.K_RIGHT]:
            x_vector += 2
        if keys_pressed[pg.K_UP]:
            y_vector -= 2
        if keys_pressed[pg.K_DOWN]:
            y_vector += 2
        if keys_pressed[pg.K_q]:
            time.sleep(10)
        player.move(x_vector,y_vector)
    enemies.move()
    screen.render(player, player_container, walls, enemies)

    pg.display.flip()
    clock.tick(60)