### Tanks game

# system imports
import sys, pygame as pg
from pygame.locals import *

# local imports
from utils.display.main import Screen
from utils.display.colours import *

from utils.player.main import Player, Create_Player

# variables
DISPLAY_BASE = 700
DISPLAY_HEIGHT = 700
GAME_BASE = 1400
GAME_HEIGHT = 1400


# classes
screen = Screen(DISPLAY_BASE,DISPLAY_HEIGHT, GAME_BASE, GAME_HEIGHT)
clock = pg.time.Clock()


player = Player(BLACK,50,50,DISPLAY_BASE, DISPLAY_HEIGHT, GAME_BASE, GAME_HEIGHT)
player_container = Create_Player(player)
# mainloop

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

    screen.fill(WHITE)

    player_container.draw(screen.DISPLAY)


    pg.display.update()
    clock.tick(60)