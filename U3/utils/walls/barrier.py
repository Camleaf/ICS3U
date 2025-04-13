import pygame as pg
from ..display.colours import *
import time
class Barrier:
    """A special type of wall which remains static at the edge of the world"""
    def __init__(self, GAME_HEIGHT, GAME_BASE):
        self.walls = [

        ]
        self.GAME_HEIGHT = GAME_HEIGHT
        self.GAME_BASE = GAME_BASE
        # format [top,left,width,height]
        self.wall_thickness = 50
        self.walls.append([0, -self.wall_thickness, self.wall_thickness, GAME_HEIGHT])
        self.walls.append([-self.wall_thickness, 0, GAME_BASE, self.wall_thickness])
        self.walls.append([0, GAME_HEIGHT, self.wall_thickness, GAME_BASE])
        self.walls.append([GAME_BASE, 0, GAME_HEIGHT, self.wall_thickness])
    
    def render(self, DISPLAY, camera_x:float, camera_y:float, DISPLAY_BASE:int, DISPLAY_HEIGHT:int):
        """Uses a static display where the coordinates of all of these are the same from round to round"""
        for top, left, width, height in self.walls:
            # If any part of the wall is visible to the player
            
            # 0 0
            # 350, 350
            # 
            
            if camera_x - DISPLAY_BASE/2 <= left <= camera_x + DISPLAY_BASE/2 or camera_y - DISPLAY_HEIGHT / 2 <= top <= camera_y + DISPLAY_HEIGHT / 2:
                # print( )
                # print(left,top)
                # print((left-camera_x+DISPLAY_BASE/2,top-camera_y+DISPLAY_HEIGHT/2))
                new_left:int = left-camera_x+DISPLAY_BASE/2
                new_top:int = top-camera_y+DISPLAY_HEIGHT/2
                new_rect = (new_left,new_top,width,height)
                pg.draw.rect(DISPLAY, BLACK, (new_left,new_top,width,height))
                 #inverts left and top from above because left is first
        
