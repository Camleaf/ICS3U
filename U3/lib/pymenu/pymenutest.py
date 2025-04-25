import pymenu as mu
import pygame as pg
from pygame.locals import *
import sys

pg.init()

# now i just need clipboard integration
display = pg.display.set_mode((400,400))
window = mu.Window(400,400, (101,101,100))

WHITE=(255,255,255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

switch = ["updates work!", "And so do grids apaprently with multi lines what does this look like"]
idx = 0
def button_test(an_arg, otherID):
    global idx
    window.update_stat(otherID, text=switch[idx])
    window.update_surf(otherID)
    idx = 1 if idx == 0 else 0



grid = mu.Grid(2,2,200,100)
label = mu.Label(window, "Colors finally work", width=170, text_size=15, border_width=3, corner_radius=2, border_color=RED, background_color=BLUE, text_color=WHITE)
grid.pack(label, 0, 0, 1, "testlabel")

label = mu.Label(window, "And so do grids apaprently with multi lines what does this look like", width=170, text_size=15, border_width=3, corner_radius=2)
grid.pack(label, 1, 1, 1, "testlabel1")

button = mu.Button(window, text="click me", command=button_test, args=("The function works!", "testlabel1"), width=170, text_size=15, border_width=3, corner_radius=2)
grid.pack(button, 0, 1, 1, "testbutton")

textbox = mu.TextBox(window, "I'm a buggy as hell textbox!", width=170, text_size=15, border_width=3, corner_radius=2)
grid.pack(textbox, 1,0,1, "textbox")


window.pack(grid, (0,0))

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            window.mouseInteraction(pg.mouse.get_pos())
        if event.type == pg.KEYDOWN:
            key = event.dict['unicode']
            if key.lower() in 'abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()-_=+|?/~.,<>;: \\\'\"' or key in ["\x08","\r", "\t"]:
                window.keyboardInteraction(key)



    display.fill(WHITE)
    display.blit(window.surface(), (0,0))
    pg.display.update()