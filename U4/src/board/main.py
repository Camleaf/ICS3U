import pygamenu as pm
from pygamenu.compiler import Element, DivElement,\
        TextElement, FrameElement, ImageElement, PolygonElement
import sys,math, pygame as pg
from pygame.locals import *
import random
import string
from ..card.main import Card, rand_str
from .deck import Deck


TRANSFORM = {
    'A': 1, # I'm going to have to add a context thing for this to see if it is a one or a 14
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 11,
    'Q': 12,
    'K': 13
}
SUITS = ['diamonds','spades','hearts','clubs']
VALID_SUIT_SWITCHES = {
    'diamonds': ['spades','clubs'],
    'spades': ['diamonds','hearts'],
    'hearts': ['spades','clubs'],
    'clubs': ['diamonds','hearts']
}

# I might just do solitaire it would be a hell of a lot easier. I also already have some stuff built out for it


class Board:
    player_positions = [0,1,2,3,4,5,6]
    ace_positions = [7,8,9,10]
    positions:list[pg.Rect]
    position_contents:dict[int,list[Card]]
    cards:list[Card]
    left_pile:list[str]
    right_pile:list[str]
    hidden_deck:list[Card]
    moving_cards:int # To track how many cards are being moved by the player at a time
    chosen:dict[str,list]
    deck:list
    deck_index:int
    deck_object:Deck
    moves:int

    def __init__(self,View:pm.View):
        self.positions = []
        self.left_pile = []
        self.cards = []
        self.right_pile = []
        self.moving_cards = 0
        self.moves = 0
        self.View = View
        self.move_holder = self.View.getStateById('moves')


        for i in range(7):
            # player side
            self.positions.append(pg.Rect(30+ i* 110,95,100,140))
        with self.View.noRender():
            for i in range(4):
                self.positions.append(pg.Rect(760+i*110,440,100,140))
                throwaway_el = self.View.createElement('div',rand_str(16),'playfield')
                throwaway_el.setstyleblock({
                    'width':'100',
                    'height':'140',
                    'background':'(0,0,0)',
                    'opacity':'50%',
                    'corner-radius':'4',
                    'top':'440',
                    'left':f'{760+i*110}'
                })
                self.View.sink(throwaway_el)
            
        # create content list
        self.position_contents = {i:[] for i in range(11)}

        self.create_board()
        self.deck_object = Deck(self.View,self)
    
    def collision(self,card:Card):
        el = card.bg
        el_rect = el.get_surface()['rect']
        collision_found = False
        for i, rct in enumerate(self.positions):
            if rct.colliderect(el_rect):
                if card.position == i:
                    continue
                
                elif i in self.ace_positions and self.moving_cards > 1:
                    continue

                y_offset = 0
                
                if len(self.position_contents[i]) > 0:
                    if self.position_contents[i][-1].shown == False:
                        # show card vs not shown
                        ...
                    else:

                        if i in self.player_positions and TRANSFORM[self.position_contents[i][-1].type] - TRANSFORM[card.type] == 1\
                            and self.position_contents[i][-1].suit in VALID_SUIT_SWITCHES[card.suit]:
                            # add offset to same card stacking
                            ...
                        elif i in self.ace_positions and TRANSFORM[self.position_contents[i][-1].type] - TRANSFORM[card.type] == -1\
                            and self.position_contents[i][-1].suit == card.suit:
                            # This is for the aces
                            ...
                        else:
                            continue

                elif len(self.position_contents[i]) == 0:
                    # check for type-specific restrictions on entry card
                    if i in self.player_positions:
                        if card.type != 'K':
                            continue
                    elif i in self.ace_positions:
                        if card.type != 'A':
                            continue

                if card.position != -1:
                    self.position_contents[card.position].remove(card)
                card.position = i
                collision_found  =True

                self.position_contents[i].append(card)
                self.reposition_shown(i)
                break
        if not collision_found:
            if card.position != -1:
                self.reposition_shown(card.position)

        else:
            self.increment_moves()
            if sum(len(self.position_contents[i]) for i in self.ace_positions) == 52:
                self.View.clear_frames()
                self.View.append_frame('winFrame')
                # gameWin code
            empty = 0
            total = 0
            for i in self.player_positions:
                total += len(self.position_contents[i])
                if len(self.position_contents[i]) == 0:
                    empty += 1
            if empty == 4 and total == 52:
                self.View.clear_frames()
                self.View.append_frame('winFrame')
                # gameWin code

                
        self.moving_cards -= 1




    def player_on_click(self,card:Card):
        # I may need to go back to the element on click handling but then send some stuff back
        # here
        index = self.position_contents[card.position].index(card)
        if not card.shown:
            # If its the last in the list
            if index == len(self.position_contents[card.position])-1:
                card.show()
                self.reposition_hidden(card.position)
                self.reposition_shown(card.position)
            return
        
        offset = 0
        for stacked_card in self.position_contents[card.position][index:]:
            stacked_card.set_draggable(offset)
            self.moving_cards += 1
            offset += 15


    def create_card(self, id_='0',position=0,suit='diamonds'):
        card = Card(self,self.View,id_,position,suit)
        card.set_position(*self.positions[card.position].center)
        self.position_contents[card.position].append(card)
        self.cards.append(card)
        self.show_top(position)


    def show_top(self,index:int):
        with self.View.noRender():
            if len(self.position_contents[index]) == 0:
                return
            
            self.position_contents[index][-1].show()
            y_offset = 0
            for i,card in enumerate(self.position_contents[index][:-1][::-1]):
                y_offset -= 15
                card.hide()
                x,y = self.positions[card.position].center
                card.set_position(x,y+y_offset)
    
    def reposition_hidden(self,index:int):
        # this doesn't seem to work
        if len(self.position_contents[index]) == 0:
            return
        y_offset = 0
        for i, card in enumerate(self.position_contents[index][::-1]):
            if not card.shown:
                y_offset -= 15
                x,y = self.positions[card.position].center
                card.set_position(x,y+y_offset)

    

    def reposition_shown(self,index:int):
        if len(self.position_contents[index]) == 0:
            return
        y_offset = 0
        with self.View.noRender():
            for i, card in enumerate(self.position_contents[index]):
                if card.shown:
                    x,y = self.positions[card.position].center
                    card.set_position(x,y+y_offset)
                    self.View.hoist(card.img)
                    y_offset += 15 if index in self.player_positions else 0
                    card.offset = y_offset
            
    def increment_moves(self):
        self.moves += 1
        if self.moves == 1:
            self.move_holder.set(f'{self.moves} move')
        else:
            self.move_holder.set(f'{self.moves} moves')

    def create_board(self):
        self.deck = list(TRANSFORM.keys()) * 4
        self.chosen = {
            x:[y for y in SUITS] for x in TRANSFORM.keys()
        }
        random.shuffle(self.deck)
        self.deck_index = 0
        for i in range(7):
            for j in range(i+1):
                suit = random.choice(self.chosen[self.deck[self.deck_index]])
                self.chosen[self.deck[self.deck_index]].remove(suit)
                self.create_card(self.deck[self.deck_index],i,suit=suit)
                self.deck_index += 1
                
        
    def restart(self):
        """Restarts the game using already existing elements"""
        # add intermission screen
        self.moves = 0
        self.move_holder.set(f'{self.moves} moves')

            


        with self.View.noRender():

            self.position_contents = {i:[] for i in range(11)}
            self.deck_object.deck = []
            self.deck_object.showing = []

            random.shuffle(self.cards)

            self.deck_index = 0

            for i in range(7):
                for j in range(i+1):
                    card = self.cards[self.deck_index]

                    card.position = i
                    card.offset = 0
                    card.board = self
                    card.set_position(*self.positions[card.position].center)
                    self.position_contents[card.position].append(card)
                    card.show()
                    self.show_top(i)

                    self.deck_index += 1
            
            for x in self.cards[self.deck_index:]:
                card = self.cards[self.deck_index]
                card.position = -1
                card.offset = 0
                card.board = self.deck_object
                card.set_position(*self.deck_object.position.center)
                self.deck_object.deck.append(card)
                card.hide()
                self.deck_index += 1
            self.View.sink(self.deck_object.clicklistener)
            self.View.sink(self.deck_object.deck_shadow)

            self.View.remove_frame('intermission')
            self.View.append_frame('background')
            self.View.append_frame('playfield')