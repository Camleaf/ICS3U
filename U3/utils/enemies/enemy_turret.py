import pygame as pg
from ..display.colours import *
import math


class Turret:
    """The turret animation for the player"""

    def __init__(self, width, height, DISPLAY_HEIGHT, DISPLAY_BASE, gun_type):

        self.rotation = 0
        self.fwidth = width
        self.fheight = height
        self.image_orig = pg.Surface([self.fwidth, self.fheight])
        self.image_orig.set_colorkey(BLACK)
        self.image_orig.fill(BLACK)
        self.gun_type = gun_type
        if self.gun_type == 'machine':
            pg.draw.rect(self.image_orig, OFF_BLACK, (self.fwidth/2 -
                        5, self.fheight/2-5, 10, 10), border_radius=4)
            pg.draw.rect(self.image_orig, OFF_BLACK, (self.fwidth/2-5,
                        self.fheight/2-30, 10, 30), border_radius=2)
        elif self.gun_type == 'shotgun':
            pg.draw.rect(self.image_orig, OFF_BLACK, (self.fwidth/2 -
                        10, self.fheight/2-10, 20, 20), border_radius=10)
            pg.draw.rect(self.image_orig, OFF_BLACK, (self.fwidth/2-10,
                        self.fheight/2-25, 20, 25), border_radius=2)
        self.image = self.image_orig.copy()

        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT
        self.DISPLAY_BASE = DISPLAY_BASE

        self.offset = (70 - self.fwidth) / 2
        self.rot_offset = 0
        # print(self.fwidth,self.fheight)
        # print(self.image.get_rect().center)
        # self.rotation = 20
        # self.rotate()
        # print(self.image.get_rect().center)
        # still has jittering on rotation due to a "well i've tried everything i can think of and this is the best result" solution to the image rescaling and rebalancing issue
        # here's desmos link to document https://www.desmos.com/calculator/unzofi1ful

    def rotation_manager(self, x, y, camera_x, camera_y):
        """Manages rotation based on the angle between the unit and the player"""

        # relative positions use the base's coords as that doesn't rely on an approximate function for positioning
        relative_x, relative_y = camera_x-x-35, camera_y-y-35

        angle = math.degrees(math.atan2(relative_y, relative_x))
        self.rotation = -angle - 90
        # print(relative_x,relative_y,angle)
        # I will need to add more complex motion predictor thing but this is okay for now
        self.rotate()

    def rotate(self):
        """Rotates the turret image to rotation"""
        self.image = pg.transform.rotate(self.image_orig, self.rotation)
        # this is the curve gained from the equations found on the desmos doc
        self.rot_offset = 12 - \
            abs(((((self.rotation % 90) / 45) - 1)**1.872) * 12)
