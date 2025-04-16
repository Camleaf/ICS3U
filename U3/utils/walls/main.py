import pygame as pg
from ..display.colours import *
import random
import os

class Walls:
    """Class which contains all the walls"""
    def __init__(self, GAME_BASE, GAME_HEIGHT, DISPLAY_BASE, DISPLAY_HEIGHT):
        self.GAME_BASE = GAME_BASE
        self.GAME_HEIGHT = GAME_HEIGHT
        self.DISPLAY_BASE = DISPLAY_BASE
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT
        self.walls = []
        self.create_walls()
        self.create_surface()

    
    def create_walls(self):
        """
        Using the recursive divison method
         - Bisects the grid twice, one x axis line and one y axis, then puts a hole in each. For each smaller chamber repeat
        """
        self.walls = set()
        self.bisect_walls((0,0,self.GAME_BASE//70, self.GAME_HEIGHT//70),3)

        self.new_walls = [x for x in self.walls]
        random.shuffle(self.new_walls)
        self.walls = []
        for i, [x,y] in enumerate(self.new_walls):
            if i%3==0: continue
            if x >= self.GAME_BASE//70 or y >= self.GAME_HEIGHT//70:
                continue
            if [x,y] == [self.GAME_BASE//140, self.GAME_HEIGHT//140]: continue
            self.walls.append([x,y])


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
        # the bisecting
        col_line = random.randint(1, width-2)
        row_line = random.randint(1, height-2)
        # the guaranteed holes to make everything accessible
        col_hole = random.randint(1,height-2)
        row_hole = random.randint(1, width-2)

        # create the column wall items
        for i in range(height):
            if i == col_hole or i == col_hole + 1: continue
            wall = (col_line+left,i+1+top)
            self.walls.add(wall)
        
        # create the row wall items
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


    def create_surface(self):
        """Creates a surface containing all wall positions for fast rendering"""
        self.tile = pg.transform.scale(pg.image.load(os.path.join('assets','walltile.jpg')), (70,70))
        self.surface = pg.Surface([self.GAME_BASE, self.GAME_HEIGHT])
        self.surface.set_colorkey((0,0,0))
        for wall in self.walls:
            x,y = wall
            # multiply by 70 as wall objects are stored relative to each other not the grid
            x *= 70
            y *= 70
            self.surface.blit(self.tile, (x,y))
        self.surface.convert()
    

    def render(self,DISPLAY, camera_x, camera_y):
        """Blits the surface to the game"""
        DISPLAY.blit(self.surface, (-camera_x+self.DISPLAY_BASE/2, -camera_y+self.DISPLAY_HEIGHT/2))

    