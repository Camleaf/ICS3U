import pygame as pg
from ..display.colours import *
import threading as th
import random

class Walls:

    def __init__(self, GAME_BASE, GAME_HEIGHT, DISPLAY_BASE, DISPLAY_HEIGHT):
        self.GAME_BASE = GAME_BASE
        self.GAME_HEIGHT = GAME_HEIGHT
        self.DISPLAY_BASE = DISPLAY_BASE
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT
        self.walls = []
        self.create_walls()

    
    def create_walls(self):
        """
        Using the recursive divison method
         - Bisects the grid twice, one x axis line and one y axis, then puts a hole in each. For each smaller chamber repeat
        """
        self.walls = set()
        self.bisect_walls((0,0,self.GAME_BASE//50, self.GAME_HEIGHT//50),2)

        self.new_walls = [x for x in self.walls]
        for i,[x,y] in enumerate(self.walls):
            if [x,y] in [self.GAME_BASE//160, self.GAME_HEIGHT//160]:
                self.new_walls.pop(i)
                break
        random.shuffle(self.new_walls)
        self.walls = [x for i,x in enumerate(self.new_walls) if i%3 != 0]


    def bisect_walls(self,chamber,level):
        """Recursive wall creation function taking 'chamber' and 'level' as input
        chamber --> (left,top,width, height) : tuple(int)
             -- all coordinates are based off the game base and height divided by 80
        level --> int
             -- The number of recursions that the wall builder should take
        
        """
        if level == 0:
            return
        # walls are built (x,y)
        left, top, width, height = chamber
        if width <= 2 or height <= 2: return
        col_line = random.randint(1, width-2)
        row_line = random.randint(1, height-2)
        col_hole = random.randint(1,height-2)
        row_hole = random.randint(1, width-2)
        for i in range(height):
            if i == col_hole or i == col_hole + 1: continue
            wall = (col_line+left,i+1+top)
            self.walls.add(wall)
        
        for i in range(width):
            if i == row_hole or i == row_hole + 1: continue
            wall = (i+1+left, row_line + top)
            self.walls.add(wall)
        
        # gets new chambers for recursive algorithm
        new_chambers = (
            (left,top,col_line-1,row_line-1),
            (left,top+row_line+1,col_line-1,height-row_line),
            (left+col_line+1,top,width-col_line, row_line-1),
            (left+col_line+1,top+row_line+1,width-col_line,height-row_line)
        )
        for cham in new_chambers:
            self.bisect_walls(cham,level-1)

    def render(self,DISPLAY, camera_x, camera_y):

        # Todo optimize the render system so that this can run on codehs
        for wall in self.walls:
            x,y = wall
            x *= 70
            y *= 70
            pg.draw.rect(DISPLAY, BLACK, (x-camera_x+self.DISPLAY_BASE/2, y-camera_y+self.DISPLAY_HEIGHT/2, 70, 70),border_radius=5)
