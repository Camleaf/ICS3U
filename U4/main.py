import pygamenu as pm
import sys,pygame as pg
from pygame.locals import *

pg.init()

View = pm.initialize('./tests/abcd.pym', [400,400])
View.append_frame('bg')
View.append_frame('welcome')
clock = pg.Clock()
display= pg.display.set_mode((400,400),pg.SRCALPHA)

text = View.getStateById('textState')
el = View.getElementById('welcome')


x = True
def myfunc(element):
    global x
    if x:
        el.setstyleattribute('background','(255,255,255)')
        x = False
    else:
        el.setstyleattribute('background','(255,0,0)')
        x = True

r = True
def myfunc2(event, global_dict):
    global r
    if r:
        text.set('Wieewwww I was updated')
        r = False
    else:
        text.set('hello I am reactive state')
        r = True
    
# View.addEventListener('keydown',myfunc2)

while True:
    display.fill((0,0,0))
    for event in pg.event.get():

        View.passEvent(event, globals())
        
        if event.type == QUIT:
            pg.quit()
            sys.exit()

        
    display.blit(View.surf,(0,0))
    pg.display.flip()
    clock.tick(24)
    