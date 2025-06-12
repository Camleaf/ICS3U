from pygamenu import initialize, View
import sys,pygame as pg
from pygame.locals import *

pg.init()

View = initialize('./tests/abcd.pym', [600,600])
View.append_frame('bg')
View.append_frame('welcome')
clock = pg.Clock()
display= pg.display.set_mode((600,600),pg.SRCALPHA)


    
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
    