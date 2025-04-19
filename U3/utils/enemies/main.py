import pygame as pg
import threading, random

from ..display.colours import *
from .enemy import Enemy
from ..walls.main import Walls
from ..bullet.main import Magazine
class Enemies:
    """Class which contains all the enemies"""
    units: list[Enemy]
    active_paths: list[threading.Thread]

    def __init__(self, enemies_num, width, height, GAME_BASE, GAME_HEIGHT, DISPLAY_BASE, DISPLAY_HEIGHT,walls:Walls, camera_x, camera_y, stocks):
        
        self.number = enemies_num
        self.active_paths = []

        self.units = []
        self.GAME_BASE = GAME_BASE
        self.GAME_HEIGHT = GAME_HEIGHT
        self.DISPLAY_BASE = DISPLAY_BASE
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT
        self.unit_width = width
        self.unit_height = height
        self.offset = (70 - self.unit_width) / 2
        self.stocks = stocks
        self.cur_id = 0
        self.walls = walls
        self.magazine = Magazine("bot",walls,GAME_BASE,GAME_HEIGHT,DISPLAY_BASE,DISPLAY_HEIGHT)
        self.create_pathfinding_grid(walls)
        self.create_units(walls, camera_x, camera_y)
        
        
    def create_indiv(self):
        """Same as create_units function but for individual units, and requiring less positional arguments. Slightly less efficient as well as can't group create"""
        # maybe as QOL later I could make it so that this function spawns units outside of the player's POV
        y = None
        x = None
        for r in range(1000):
            ry = random.randint(0,self.GAME_HEIGHT//70 - 1)
            rx = random.randint(0, self.GAME_BASE // 70 - 1)
            if [rx,ry] in self.walls.walls:
                continue
            if any([round(unit.x//70), round(unit.y//70)] == [rx,ry] for unit in self.units):
                
                continue
            y = ry
            x = rx
        self.cur_id += 1
        if self.stocks == 0: return
        self.stocks -= 1
        self.units.append(
                Enemy( self.unit_width, 
                      self.unit_height, 
                      x*70,
                      y*70, 
                      self.DISPLAY_HEIGHT, 
                      self.DISPLAY_BASE, 
                      self.GAME_BASE, 
                      self.GAME_HEIGHT,
                      0,
                      0,
                      self.grid,
                      self.offset,
                      self.cur_id
                      )
        )
                    
    def create_units(self,walls:Walls ,camera_x, camera_y):
        """Creates the enemy class self.number and stores them in a wrapper"""
        already_created = []
        for i in range(self.number):
            x = None
            y = None
            for r in range(1000):
                ry = random.randint(0,self.GAME_HEIGHT//70 - 1)
                rx = random.randint(0, self.GAME_BASE // 70 - 1)
                if [rx,ry] in walls.walls:
                    continue
                if [rx,ry] in already_created:
                    continue
                if ry > 4 and not ry > 13:continue
                elif rx > 4 and not rx > 13: continue
                y = ry
                x = rx
                break
            self.cur_id = i
            self.stocks -= 1
            already_created.append([x,y])
            self.units.append(
                Enemy( self.unit_width, 
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
                      self.offset,
                      i
                      )
            )
    
        
    def destroy_unit(self,id):
        new = []
        for unit in self.units:
            if unit.id != id:
                new.append(unit)
        self.units = new
        if self.stocks != 0:
            self.create_indiv()
        

    def move(self,player):
        self.magazine.update_bullets(self,player)
        for i in range(len(self.units)):
            self.units[i].move(self.units)

    def render(self, DISPLAY, camera_x, camera_y):
        # very much a temporary render function
        for unit in self.units:
            #print(unit.x-camera_x+self.GAME_BASE//2, unit.y-camera_y+self.GAME_HEIGHT//2)
            unit.player_pass(camera_x,camera_y)

            DISPLAY.blit(unit.image, (unit.x-camera_x+self.DISPLAY_BASE//2+self.offset-unit.rot_offset, unit.y-camera_y+self.DISPLAY_HEIGHT//2+self.offset-unit.rot_offset))
            DISPLAY.blit(unit.turret.image, (unit.x-camera_x+self.DISPLAY_BASE//2+unit.turret.offset-unit.turret.rot_offset, unit.y-camera_y+self.DISPLAY_HEIGHT//2+unit.turret.offset-unit.turret.rot_offset))
        

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
    
    def check_shots(self,tick):
            for unit in self.units:
                if unit.activated:
                    if tick <= 5: continue
                    if unit.shot_cooldown < 20: 
                        unit.shot_cooldown += 1
                        continue
                    unit.shot_cooldown  = 0
                    if unit.raycast(self.magazine.bullet_speed):
                        self.magazine.create_bullet(unit.turret.rotation,unit.x+35-unit.rot_offset,unit.y+35-unit.rot_offset)
