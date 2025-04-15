import pygame as pg
import threading, random

from ..display.colours import *
from .enemy import Enemy
from ..walls.main import Walls
class Enemies:
    """Class which contains all the enemies"""
    units: list[Enemy]
    active_paths: list[threading.Thread]

    def __init__(self, enemies_num, width, height, GAME_BASE, GAME_HEIGHT, DISPLAY_BASE, DISPLAY_HEIGHT,walls:Walls, camera_x, camera_y):
        
        self.number = enemies_num
        self.active_paths = []

        self.units = []
        self.GAME_BASE = GAME_BASE
        self.GAME_HEIGHT = GAME_HEIGHT
        self.DISPLAY_BASE = DISPLAY_BASE
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT
        self.unit_width = width
        self.unit_height = height
        self.create_pathfinding_grid(walls)
        self.create_units(walls, camera_x, camera_y)
        

    def create_units(self,walls:Walls ,camera_x, camera_y):
        """Creates the enemy class self.number and stores them in a wrapper"""
        for i in range(self.number):
            x = None
            y = None
            for r in range(1000):
                ry = random.randint(0,self.GAME_HEIGHT//70 - 1)
                rx = random.randint(0, self.GAME_BASE // 70 - 1)
                if [rx,ry] in walls.walls:
                    continue
                y = ry
                x = rx
                break

            self.units.append(
                Enemy(RED, 
                      self.unit_width, 
                      self.unit_height, 
                      x*70,
                      y*70, 
                      self.DISPLAY_HEIGHT, 
                      self.DISPLAY_BASE, 
                      self.GAME_BASE, 
                      self.GAME_HEIGHT,
                      camera_x,
                      camera_y,
                      self.grid,
                      i
                      )
            )
    
        

    def move(self):
        for i in range(len(self.units)):
            self.units[i].move(self.units)

    def render(self, DISPLAY, camera_x, camera_y):
        # very much a temporary render function
        for unit in self.units:
            #print(unit.x-camera_x+self.GAME_BASE//2, unit.y-camera_y+self.GAME_HEIGHT//2)
            unit.player_pass(camera_x,camera_y)
            
            DISPLAY.blit(unit.image, (unit.x-camera_x+self.DISPLAY_BASE//2+(35/2), unit.y-camera_y+self.DISPLAY_HEIGHT//2+(35/2)))
    
    def create_pathfinding_grid(self, walls):
        self.grid = []
        for y in range(self.GAME_HEIGHT//70):
            temp = []
            for x in range(self.GAME_BASE//70):
                if [x,y] in walls.walls:
                    temp.append(1)
                else:
                    temp.append(0)
            self.grid.append(temp)