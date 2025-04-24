import pymenu as mu
import pygame as pg
from pygame.locals import *
import sys

pg.init()

# this code (lines 9-21) runs like 250 lines behind the scenes
display = pg.display.set_mode((400,400))
window = mu.Window(400,400, (101,101,100))

WHITE=(255,255,255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

grid = mu.Grid(2,2,200,100)
label = mu.Label(window, "Colors finally work", width=170, text_size=15, border_width=3, corner_radius=2, border_color=RED, background_color=BLUE, text_color=WHITE)
grid.pack(label, 0, 0, 1, "testlabel")

label = mu.Label(window, "And so do grids", width=170, text_size=15, border_width=3, corner_radius=2)
grid.pack(label, 1, 1, 1, "testlabel1")

window.pack(grid, (0,0))

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
    display.fill(WHITE)
    display.blit(window.surface(), (0,0))
    pg.display.update()