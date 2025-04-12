
# system imports
import sys, pygame as pg
from pygame.locals import *

# local imports
from utils.display.main import Display
from utils.display.colours import *

# variables
DISPLAY_BASE = 500
DISPLAY_HEIGHT = 500

# classes
display = Display(DISPLAY_BASE,DISPLAY_HEIGHT)


# mainloop
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
    display.fill(WHITE)
    pg.display.update()