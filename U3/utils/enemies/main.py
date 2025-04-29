import pygame as pg
import threading
import random

from ..display.colours import *
from .enemy import Enemy
from ..walls.main import Walls
from ..bullet.main import Magazine


class Enemies:
    """Class which contains all the enemies"""
    units: list[Enemy]
    active_paths: list[threading.Thread]
    diff_presets = {
        1:{"stocks":3, "number":2, "gold_mult":0.5,"bdist_mult":0.9, "shotgun%":1}, # add type of guns to be used
        2:{"stocks":6, "number":3, "gold_mult":0.7,"bdist_mult":0.9, "shotgun%":7}, # add shotgun functionality
        3:{"stocks":8, "number":4, "gold_mult":1,"bdist_mult":1, "shotgun%":10},
        4:{"stocks":10, "number":4, "gold_mult":1.2,"bdist_mult":1.1, "shotgun%":12},
        5:{"stocks":15, "number":5, "gold_mult":1.6,"bdist_mult":1.5, "shotgun%":22},
        6:{"stocks":15, "number":10, "gold_mult":2.2,"bdist_mult":1.6, "shotgun%":40},
        7:{"stocks":25, "number":15, "gold_mult":3, "bdist_mult":1.8, "shotgun%":50},
    }


    def __init__(self, width, height, GAME_BASE, GAME_HEIGHT, DISPLAY_BASE, DISPLAY_HEIGHT, walls: Walls, camera_x, camera_y, difficulty, death_value:int=100):

        self.difficulty = difficulty
        self.active_paths = []
        self.units = []
        self.GAME_BASE = GAME_BASE
        self.GAME_HEIGHT = GAME_HEIGHT
        self.DISPLAY_BASE = DISPLAY_BASE
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT
        self.unit_width = width
        self.unit_height = height
        self.offset = (70 - self.unit_width) / 2
        self.number = self.diff_presets[difficulty]["number"]
        self.stocks = self.diff_presets[difficulty]["stocks"]
        self.orig_stocks = self.stocks
        self.camera_x = GAME_BASE/2
        self.camera_y = GAME_HEIGHT/2
        self.death_value = int(death_value * self.diff_presets[difficulty]["gold_mult"])
        self.cur_id = 0
        self.walls = walls
        self.current_gold_increase = 0
        # init the surface which holds the image of all the dead enemies
        self.dead_surf: pg.Surface = pg.Surface([GAME_BASE, GAME_HEIGHT])
        self.dead_surf.set_colorkey((255, 255, 255))
        self.dead_surf.fill(WHITE)
        # end init
        self.magazine = Magazine(
            "bot", walls, GAME_BASE, GAME_HEIGHT, DISPLAY_BASE, DISPLAY_HEIGHT, self.diff_presets[difficulty]["bdist_mult"])
        self.create_pathfinding_grid(walls)
        self.create_units(walls, camera_x, camera_y)

    def create_indiv(self):
        """Same as create_units function but for individual units, and requiring less positional arguments. Slightly less efficient as well as can't group create"""
        # maybe as QOL later I could make it so that this function spawns units outside of the player's POV
        y = None
        x = None
        for r in range(10000):
            ry = random.randint(0, self.GAME_HEIGHT//70 - 1)
            rx = random.randint(0, self.GAME_BASE // 70 - 1)
            if [rx, ry] in self.walls.walls:
                continue
            if any([round(unit.x//70), round(unit.y//70)] == [rx, ry] for unit in self.units):

                continue
            if abs(rx-(self.camera_x//70)) + abs(ry-(self.camera_y//70)) < 8:
                continue
            y = ry
            x = rx
            break
        self.cur_id += 1
        if self.stocks == 0:
            return
        self.stocks -= 1
        self.units.append(
            Enemy(self.unit_width,
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
    def end_game(self):
        return {"increase":self.current_gold_increase, "repair_cost": self.death_value*self.orig_stocks//2}

    def create_units(self, walls: Walls, camera_x, camera_y):
        """Creates the enemy class self.number and stores them in a wrapper"""
        already_created = []
        for i in range(self.number):
            x = None
            y = None
            for r in range(1000):
                ry = random.randint(0, self.GAME_HEIGHT//70 - 1)
                rx = random.randint(0, self.GAME_BASE // 70 - 1)
                if [rx, ry] in walls.walls:
                    continue
                if [rx, ry] in already_created:
                    continue
                if ry > 4 and not ry > 13:
                    continue
                elif rx > 4 and not rx > 13:
                    continue
                y = ry
                x = rx
                break
            self.cur_id = i
            self.stocks -= 1
            already_created.append([x, y])
            self.units.append(
                Enemy(self.unit_width,
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

    def destroy_unit(self, id):
        new = []
        for unit in self.units:
            if unit.id != id:
                new.append(unit)
            else:
                self.add_to_dead(unit)

        self.units = new
        if self.stocks != 0:
            self.create_indiv()  # add cam x and cam y to this
        self.current_gold_increase += self.death_value

    def add_to_dead(self, unit: Enemy):
        unit.image_orig = pg.Surface([unit.width, unit.height])
        unit.image_orig.set_colorkey((255, 255, 255))
        unit.image_orig.fill(WHITE)

        pg.draw.rect(unit.image_orig, OFF_BLACK,
                     (0, 1, unit.width, unit.height-2), border_radius=2)
        pg.draw.rect(unit.image_orig, BLACK,
                     (7, 0, unit.width-14, unit.height), border_radius=2)
        pg.draw.rect(unit.image_orig, BLACK, (unit.width/2-10,
                     unit.height/2-15, 20, 30), border_radius=2)
        unit.rotate(0)

        self.dead_surf.blit(unit.image, (unit.x+unit.offset -
                            unit.rot_offset, unit.y+unit.offset-unit.rot_offset))
        self.dead_surf.blit(unit.turret.image, (unit.x+unit.turret.offset -
                            unit.turret.rot_offset, unit.y+unit.turret.offset-unit.turret.rot_offset))

    def move(self, player):
        self.magazine.update_bullets(self, player)
        for i in range(len(self.units)):
            self.units[i].move(self.units)

    def render(self, DISPLAY: pg.Surface, camera_x: int, camera_y: int):
        self.camera_x = camera_x
        self.camera_y = camera_y
        # very much a temporary render function
        DISPLAY.blit(self.dead_surf, (-camera_x+self.DISPLAY_BASE /
                     2, -camera_y+self.DISPLAY_HEIGHT/2))
        for unit in self.units:
            # print(unit.x-camera_x+self.GAME_BASE//2, unit.y-camera_y+self.GAME_HEIGHT//2)
            unit.player_pass(camera_x, camera_y)

            DISPLAY.blit(unit.image, (unit.x-camera_x+self.DISPLAY_BASE//2+self.offset -
                         unit.rot_offset, unit.y-camera_y+self.DISPLAY_HEIGHT//2+self.offset-unit.rot_offset))
            DISPLAY.blit(unit.turret.image, (unit.x-camera_x+self.DISPLAY_BASE//2+unit.turret.offset -
                         unit.turret.rot_offset, unit.y-camera_y+self.DISPLAY_HEIGHT//2+unit.turret.offset-unit.turret.rot_offset))

    def create_pathfinding_grid(self, walls):
        self.grid = []
        for y in range(self.GAME_HEIGHT//70):
            temp = []
            for x in range(self.GAME_BASE//70):
                if [x, y] in walls.walls:
                    temp.append(1)
                else:
                    temp.append(0)
            self.grid.append(temp)

    def check_shots(self, tick):
        for unit in self.units:
            if unit.activated:
                if tick <= 3:
                    continue
                if unit.shot_cooldown < 20:
                    unit.shot_cooldown += 1
                    continue
                unit.shot_cooldown = 0
                if unit.raycast(self.magazine.bullet_speed):
                    self.magazine.create_bullet(
                        unit.turret.rotation, unit.x+35-unit.rot_offset, unit.y+35-unit.rot_offset)
