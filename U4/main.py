"""Please don't begin this until you have received your peer feedback!"""

# This will not run here
# because of lag and the pygame-ce 
# dependency

import sys,math, pygame as pg
import pygamenu as pm
from pygamenu.compiler import Element, DivElement,\
        TextElement, FrameElement, ImageElement, PolygonElement
from pygame.locals import *

# My game will be the card game speed

from src.board.main import Board
pg.init()

View = pm.initialize('./src/pym_files/main.pym', [1200,600])
View.append_frame('welcome')
clock = pg.Clock()
display= pg.display.set_mode((1200,600),pg.SRCALPHA)

board = Board(View)

# I need something to hoist something to the top of its specific render list

name = View.getStateById('name')

def to_instructions(element:Element):
    View.remove_frame('welcome')
    View.append_frame('instructions')

def start_game(element:Element):
    input_text:TextElement = View.getElementById('nameinput')
    if input_text.text != '':
        name.set(input_text.text)
    View.remove_frame('instructions')
    View.append_frame('background')
    View.append_frame('playfield')

def restart_game(element:Element):
    View.remove_frame('playfield')
    View.remove_frame('background')
    View.append_frame('intermission')
    display.fill(color=(0, 109, 173))
    display.blit(bg,bg_rect)
    display.blit(View.surf,(0,0))
    pg.display.flip()
    board.restart()


bg = pg.Surface([1200,270])
bg.fill((102, 54, 37))
bg_rect = bg.get_rect(center=(
    600,300
))

while True:
    display.fill(color=(0, 109, 173))
    display.blit(bg,bg_rect)
    for event in pg.event.get():

        View.passEvent(event, globals())
        
        if event.type == QUIT:
            pg.quit()
            sys.exit()

    
    display.blit(View.surf,(0,0))
    pg.display.flip()
    clock.tick(60)