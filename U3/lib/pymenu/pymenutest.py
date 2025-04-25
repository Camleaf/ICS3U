import pymenu as mu
import pygame as pg
from pygame.locals import *
import sys

pg.init()

# now i just need clipboard integration
display = pg.display.set_mode((400,400))
window = mu.Window(400,400, (101,101,100))
clock = pg.Clock()

WHITE=(255,255,255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

switch = ["Overwrites work", "Hehehehehehheehe"]
idx = 0
def button_test(an_arg, otherID):
    global idx
    print(an_arg)
    window.update_stat(otherID, text=switch[idx])
    window.update_surf(otherID)
    idx = 1 if idx == 0 else 0



grid = mu.Grid(4,2,100,100)
label = mu.Label(window, "Colors finally work", width=170, text_size=15, border_width=3, corner_radius=2, border_color=RED, background_color=BLUE, text_color=WHITE)
grid.pack(label, column=0, row=0, columnspan=2, ID="testlabel")

label = mu.Label(window, "Next to me is a checkbox", width=70, text_size=15, border_width=3, corner_radius=2)
grid.pack(label, column=2, row=1, columnspan=1, ID="testlabel1")

label = mu.CheckBox(window, value=False, width=20, height=20, border_width=1, corner_radius=10)
grid.pack(label, column=3, row=1, columnspan=1, ID="testcheckbox")

button = mu.Button(window, text="click me", command=button_test, args=("The function works!", "testlabel"), width=170, text_size=15, border_width=3, corner_radius=2)
grid.pack(button, column=2, row=0, columnspan=2, ID="testbutton")

textbox = mu.TextBox(window, "I'm a buggy as hell textbox!", width=170, max_rows=3, text_size=15, border_width=3, corner_radius=2)
grid.pack(textbox, column=0,row=1,columnspan=2, ID="textbox")

frame_ids = ["f1", "f2"]
current_frame = 0
window.pack(grid, (0,0))
tick = 0
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            window.mouseInteraction(pg.mouse.get_pos())
        if event.type == pg.KEYDOWN:
            
            key = event.dict['unicode']
            
            if key.lower() in 'abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()-_=+|?/~.,<>;: ' or key in ["\r", "\t"]:
                window.keyboardInteraction(key)
            
    keys = pg.key.get_pressed()
    
    if keys[pg.K_BACKSPACE] and tick == 3: # delete letter key
        tick = 0 
        window.keyboardInteraction("\x08")
    elif keys[pg.K_LEFT] and tick == 3: # demonstrates textbox cursor moving left
        tick = 0
        window.keyboardInteraction("lspr")
    elif keys[pg.K_RIGHT] and tick == 3: # demonstrates textbox cursor moving right
        tick = 0
        window.keyboardInteraction("rspr")
    elif keys[pg.K_RIGHTBRACKET] and tick ==3: # demonstrates frame save feature
        tick =0
        window.save_frame(frame_ids[current_frame])
        current_frame = 1 if current_frame == 0 else 0
    elif keys[pg.K_LEFTBRACKET] and tick == 3: # demonstrates frame load
        
        window.load_frame(frame_ids[0])
        tick = 0



    display.fill(WHITE)
    display.blit(window.surface(), (0,0))
    if tick < 3:
        tick += 1
    pg.display.flip()
    clock.tick(24)