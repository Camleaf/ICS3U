from ..display.colours import *
from .bullet import Bullet

class Magazine:
    """Container for all the bullets"""

    def __init__(self, owner, player, enemies, walls, GAME_BASE, GAME_HEIGHT, DISPLAY_BASE, DISPLAY_HEIGHT):

        self.magazine:list[Bullet] = []
        self.GAME_BASE = GAME_BASE
        self.GAME_HEIGHT = GAME_HEIGHT
        self.DISPLAY_BASE = DISPLAY_BASE
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT
        self.owner = owner
        self.walls = walls.walls
        self.targets = []
        if owner == "player":
            for unit in enemies.units:
                self.targets.append((unit.x, unit.y))
            
        else:
            self.targets = [(player.camera_x-player.width//2, player.camera_y-player.height//2)] # all coordinates will be based off of top left so that writing code later is easier

    def create_bullet(self,angle, x, y): # x,y refers to centre of playing object
        start = (x, y)
        self.magazine.append(
            Bullet(
                3,
                3,
                self.owner,
                5,
                angle,
                start,
                self.targets,
                self.walls
            )
        )
    
    def render(self, DISPLAY):
        for bullet in self.magazine:
            DISPLAY.blit(DISPLAY, (bullet.x,bullet.y))
            