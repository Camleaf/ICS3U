from ..display.colours import *
from .bullet import Bullet

class Magazine:
    """Container for all the bullets"""

    def __init__(self, owner, walls, GAME_BASE, GAME_HEIGHT, DISPLAY_BASE, DISPLAY_HEIGHT, dist_mult=1):

        self.magazine:list[Bullet] = []
        self.GAME_BASE = GAME_BASE
        self.GAME_HEIGHT = GAME_HEIGHT
        self.DISPLAY_BASE = DISPLAY_BASE
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT
        self.owner = owner
        self.walls = walls.walls
        self.bullet_speed = 8
        self.bullet_base_distance = 300 * dist_mult
         # all coordinates will be based off of top left so that writing code later is easier
        self.create_grid()


    def create_bullet(self,angle, x, y, mult=1): # x,y refers to centre of playing object
        # if i need ideas for any QOL stuff make it so the bullet spawns at the end of the turret not the centre of the tank
        self.magazine.append(
            Bullet(
                8,
                8,
                self.owner,
                self.bullet_speed,
                angle,
                (x, y),
                self.grid,
                self.bullet_base_distance*mult
            )
        )
    def update_bullets(self, enemies, player):
        self.targets = []
        if self.owner == "player": # recalculate targets every runthrough
            for unit in enemies.units:
                self.targets.append(unit)
            
        else:
            self.targets = [(player.camera_x-player.width//2, player.camera_y-player.height//2)]

        r = len(self.magazine)
        new = []
        for i in range(r):
            if not self.magazine[i].move(self.targets, enemies, player):
                new.append(self.magazine[i])
        self.magazine = new
            
    def create_grid(self):
        self.grid = []
        for y in range(self.GAME_HEIGHT//70):
            temp = []
            for x in range(self.GAME_BASE//70):
                if [x,y] in self.walls:
                    temp.append(1)
                else:
                    temp.append(0)
            self.grid.append(temp)

    def render(self, DISPLAY, camera_x, camera_y):
        for bullet in self.magazine:
            DISPLAY.blit(bullet.image, (bullet.x-camera_x+self.DISPLAY_BASE//2,bullet.y-camera_y+self.DISPLAY_HEIGHT//2))
            