import pygame as pg
import threading

from ..display.colours import *
from .enemy import Enemy

class Enemies:
    """Class which contains all the enemies"""
    units: list[Enemy]
    active_paths: list[threading.Thread]

    def __init__(self, enemies_num, width, height, GAME_BASE, GAME_HEIGHT, DISPLAY_BASE, DISPLAY_HEIGHT):
        
        self.number = enemies_num
        self.active_paths = []

        self.units = []
        self.GAME_BASE = GAME_BASE
        self.GAME_HEIGHT = GAME_HEIGHT
        self.DISPLAY_BASE = DISPLAY_BASE
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT
        self.unit_width = width
        self.unit_height = height
        self.create_units()

    def create_units(self):
        """Creates the enemy class self.number and stores them in a wrapper"""
        for i in range(self.number):
            self.units.append(
                Enemy(RED, 
                      self.unit_width, 
                      self.unit_height, 
                      100, # xpos. Temporary until I make a placement function
                      100, # ypos. Temporary until I make a placement function
                      self.DISPLAY_HEIGHT, 
                      self.DISPLAY_BASE, 
                      self.GAME_BASE, 
                      self.GAME_HEIGHT)
            )
    def render(self, DISPLAY, camera_x, camera_y):
        # very much a temporary render function
        for unit in self.units:
            print(unit.x-camera_x+self.GAME_BASE//2, unit.y-camera_y+self.GAME_HEIGHT//2)
            DISPLAY.blit(unit.image, (unit.x-camera_x+self.GAME_BASE//2, unit.y-camera_y+self.GAME_HEIGHT//2))