import menutils as mu
import pygame as pg
from pygame.locals import *
import sys

pg.init()

display = pg.display.set_mode((300,300))
window = mu.Window(100,100, (101,101,100))

WHITE=(255,255,255)
label = mu.Label(window, "Hello yes I would like to do the coding", width=90, text_padding=4, text_size=20, border_width=3, corner_radius=5)
window.pack(label, (0,0))


while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
    display.fill(WHITE)
    display.blit(window.surface(), (0,0))
    pg.display.update()