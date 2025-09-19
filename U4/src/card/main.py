import pygamenu as pm
from pygamenu.compiler import Element, DivElement,\
        TextElement, FrameElement, ImageElement, PolygonElement
import sys,math, pygame as pg

from pygame.locals import *
import random
import string


NAME_TRANSFORM = {
    'A':'ace',
    'J':'jack',
    'K':'king',
    'Q':'queen'
}


class Card:
    ids: list[str]
    # add red and black generation here

    bg: DivElement
    View:pm.View
    position:int
    facedDown: DivElement
    img:ImageElement
    shown: bool
    suit:str

    def __init__(self,board,View:pm.View,type_='2',position=0,suit='diamonds'):
        self.ids = []
        self.position = position
        self.type = type_
        self.board = board
        self.View:pm.View = View
        self.shown = True
        self.offset = 0
        self.suit = suit

        with self.View.noRender():


            self.ids.append('card'+rand_str(16))
            self.bg = View.createElement('div',self.ids[-1],parent_id='playfield')
        
            self.bg.setstyleblock({
                'width':'100',
                'height':'140',
                'opacity':'0',
            })

            self.ids.append('card'+rand_str(16))
            self.facedDown = View.createElement('div',self.ids[-1],parent_id=self.ids[0])
        
            self.facedDown.setstyleblock({
                'width':'100',
                'height':'140',
                'background':'(255,100,100)',
                'border-width':'3',
                'border-color':'(100,100,100)',
                'opacity':'0',
            })



            self.ids.append('card'+rand_str(16))
            self.img:ImageElement = View.createElement('image',self.ids[-1],parent_id=self.ids[0])

            self.img.setstyleblock({
                'width':'100',
                'height':'140',
                'opacity':'255',
            })
            if self.type in ['J','K','Q']:
                self.img.setattribute('src',f'./assets/card/{NAME_TRANSFORM[self.type]}_of_{suit}.png')
            elif self.type in ['A']:
                self.img.setattribute('src',f'./assets/card/{NAME_TRANSFORM[self.type]}_of_{suit}.png')
            else:
                self.img.setattribute('src',f'./assets/card/{self.type}_of_{suit}.png')
                

            self.img.onclick.append(self.on_click)
            self.img.clickable = True

    def on_click(self, element):
        self.board.player_on_click(self)

    def set_position(self,x:int,y:int):
        # make there be an offset so that the mouse clicking and dragging has keeps relative
        # to cx and cy
        # self.View.withNoUpdate()
        with self.View.noRender():
            self.bg.setstyleblock({
                'width':'100',
                'height':'140',
                'opacity':'0',
                'cx':f'{x}',
                'cy':f'{y}'
            })
            self.img.__oncallback__()
            self.facedDown.__oncallback__()

    def hide(self):
        with self.View.noRender():
            # self.mainText.setstyleattribute('opacity','0')
            # self.displayPoly.setstyleattribute('opacity','0')
            # self.invertedMainText.setstyleattribute('opacity','0')
            
            self.bg.setstyleattribute('opacity','0')
            self.View.sink(self.img)
            self.facedDown.setstyleattribute('opacity','255')
            self.View.sink(self.bg)
            self.shown = False
    
    def show(self):
        with self.View.noRender():

            self.bg.setstyleattribute('opacity','255')
            self.facedDown.setstyleattribute('opacity','0')
            self.View.hoist(self.img)
            self.View.hoist(self.bg)
            self.shown = True

    def destroy(self):
        self.View.deleteElement(self.ids[0])
        del self


    def set_draggable(self,offset = 0):
        self.View.addEventListener('mousemove',self.on_motion)
        self.View.addEventListener('mouseup',self.release_drag)
        self.View.hoist(self.bg)
    
    def on_motion(self, event,global_dict):
        x,y = pg.mouse.get_pos()
        self.set_position(x,y+self.offset)

    def release_drag(self,event, global_dict):
        self.View.killEventListener('mousemove',self.on_motion)

        self.View.killEventListener('mouseup',self.release_drag)

        self.board.collision(self)
    


def rand_str(length):
    letters = string.ascii_lowercase
    res = ''.join(random.choice(letters) for i in range(length))
    return res