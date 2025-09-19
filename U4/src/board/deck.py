import pygamenu as pm
from pygamenu.compiler import Element, DivElement,\
        TextElement, FrameElement, ImageElement, PolygonElement
import sys,math, pygame as pg
from pygame.locals import *
import random
import string
from ..card.main import Card, rand_str



class Deck:
    """Controls the deck, also mimics the board inside of cards to not modify those too much"""
    deck:list[Card]
    position:pg.Rect
    clicklistener:TextElement
    deck_shadow:DivElement
    showing:list[Card] # showing is its own list because of the inverse 3 increments that flipping the deck needs

    def __init__(self,View:pm.View, board):
        self.View = View
        self.board = board
        self.deck = []
        self.showing = []

        with self.View.noRender():
            self.position = pg.Rect(1090,230,100,140)
            self.deck_shadow = self.View.createElement('div',rand_str(16),'playfield')
            self.deck_shadow.setstyleblock({
                'width':'100',
                'height':'140',
                'background':'(0,0,0)',
                'opacity':'40%',
                'corner-radius':'4',
                'top':'230',
                'left':f'{1090}'
            })
            self.clicklistener = self.View.createElement('text',rand_str(16),'playfield')
            self.clicklistener.setstyleblock({
                'width':'100',
                'height':'140',
                'background':'(0,0,0)',
                'opacity':'0%',
                'corner-radius':'4',
                'top':'230',
                'left':f'{1090}'
            })
            self.clicklistener.onclick.append(self.clicked_empty)
            self.clicklistener.clickable = True
        self.create_deck_object()
        self.View.sink(self.clicklistener)
        self.View.sink(self.deck_shadow)

    def create_card(self, id_='0',position=0,suit='diamonds'):
        card = Card(self,self.View,id_,position,suit)
        card.set_position(*self.position.center)
        self.deck.append(card)
        self.board.cards.append(card)
        card.hide()



    def clicked_empty(self,el):
        for card in self.deck:
            card.hide()
            card.set_position(*self.position.center)
        self.View.sink(self.clicklistener)
        self.View.sink(self.deck_shadow)
        self.showing = []

    def player_on_click(self,card:Card):
        # mimic function to hijack off the existing card callbacks without changing it too much.
        if not card.shown:
            idx = self.deck.index(card)
            card.show()
            card.set_position(980,290)
            self.showing.append(card)
            for i in range(1,3):
                if idx + i > len(self.deck)-1:
                    break
                new_card = self.deck[idx+i]
                new_card.show()
                new_card.set_position(980+i*20,290+i*10)
                self.showing.append(new_card)

        
        else:

            idx = self.showing.index(card)

            if idx != len(self.showing)-1: # If it's not on the top
                return
            
            card.set_draggable(0)
            card.orig_pos = tuple(map(int,[card.bg.getstyleattribute('cx'),card.bg.getstyleattribute('cy')]))
            # the line above was kind of bad practice because its not defined anywhere in the actual class
            # but i don't think i'll be touching the class again too much and im tired so its fine

    def collision(self, card:Card):
        
        self.board.collision(card) # this function will have a special exception for this case

        if card.position == -1:
            # If no collision was found
            card.set_position(*card.orig_pos)
            return
        
        card.board = self.board
        self.showing.remove(card)
        self.deck.remove(card)

        

        

            

            
        # now i need to make the handler for if it does show

            





    def create_deck_object(self):
        for x in [x for x in self.board.deck[self.board.deck_index:]]:
            suit = random.choice(self.board.chosen[self.board.deck[self.board.deck_index]])
            self.board.chosen[self.board.deck[self.board.deck_index]].remove(suit)
            self.create_card(x,-1,suit)
            self.board.deck_index += 1