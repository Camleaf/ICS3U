import sys,time,threading, pygame as pg
from lib.pymenu import pymenu as mu
from pygame.locals import *



from utils.container.container import Container
from utils.menu.main import Menu
from utils.display.colours import *

DISPLAY_BASE = 700
DISPLAY_HEIGHT = 700

pg.init()
clock = pg.time.Clock()


c:Container = Container(DISPLAY_BASE, DISPLAY_HEIGHT)
menu:Menu = Menu(DISPLAY_BASE, DISPLAY_HEIGHT, c)


# mainloop vars
frames_num = 1
tick = 0

menu_input_timer = 0

# mainloop

while True:

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            menu.window.mouseInteraction(pg.mouse.get_pos())
                
        # This code needs handling for backspace and stuff but I'll blow up that bridge when I get to it
        if event.type == pg.KEYDOWN:
            
            key = event.dict['unicode']
            menu.window.keyboardInteraction(key)




    c.screen.fill(BLACK)

    if keys_pressed := pg.key.get_pressed():
        # Add textbox interactions alter
        ...
        
        

                


    # run all the time
    c.screen.render(menu)


    pg.display.flip()
    

    if tick == 0:
        print(f"{frames_num} second")
        frames_num += 1
    tick += 1
    tick %= 60
    if menu_input_timer < 11:
        menu_input_timer += 1
    clock.tick(60)