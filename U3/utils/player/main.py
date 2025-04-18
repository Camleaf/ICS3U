import pygame as pg
from ..display.colours import *
from ..walls.main import Walls
from ..enemies.enemy import Enemy
from .turret import Turret
import math, time

class Player(pg.sprite.Sprite):
    """The player. Contains functions
      - __init__ | initializes the function
      - move | moves the player
    """
    image: pg.Surface
    xpos: float
    ypos: float

    def __init__(self, width:int, height:int, DISPLAY_BASE:int, DISPLAY_HEIGHT:int, GAME_BASE:int, GAME_HEIGHT:int):
      pg.sprite.Sprite.__init__(self)



      # image origin
      self.image_orig = pg.Surface([width,height])
      self.image_orig.set_colorkey((255,255,255))
      self.image_orig.fill(WHITE)
     
      pg.draw.rect(self.image_orig,OFF_BLACK, (0, 1, width, height-2), border_radius=2)
      pg.draw.rect(self.image_orig, PICKLE_GREEN, (7,0,width-14,height),border_radius=2)
      pg.draw.rect(self.image_orig,DARK_PICKLE_GREEN,(width/2-10, height/2-15,20,30),border_radius=2)
      #pg.draw.rect(self.image_orig, PICKLE_GREEN, (0,0,width,height))
      # self.image_orig.blit()
      self.image = self.image_orig.copy()
      self.rect = self.image.get_rect()
      self.rect.center = (DISPLAY_BASE/2, DISPLAY_HEIGHT/2)
      # self.rect is used for rotating, but for collisions i need a bounding box as the rect slightly deforms with rotation causing clipping issues
      self.bounding_box = self.rect.copy()


      self.turret = Turret(width+20,height+20,DISPLAY_HEIGHT,DISPLAY_BASE)


      self.DISPLAY_BASE = DISPLAY_BASE
      self.DISPLAY_HEIGHT = DISPLAY_HEIGHT
      self.width = width
      self.height = height
      self.GAME_BASE = GAME_BASE
      self.GAME_HEIGHT = GAME_HEIGHT
      self.rotation = 180
      self.camera_x = GAME_BASE/2
      self.camera_y = GAME_HEIGHT / 2
      self.rotation_target = 180
      self.prev_case = 180
      self.difference = 0
      self.in_range = []
      self.is_alive = True

    def move(self, x, y, units):
        self.turret.rotation_manager() #may have to optimize so that this doesn't run every time but for now it should work
       
        if self.width/2 < self.camera_x + x < self.GAME_BASE - self.width/2:
            self.camera_x += x
   
        if self.collision(x,0,1,units):
           x = 0
        
        if self.height/2 < self.camera_y + y < self.GAME_HEIGHT - self.height/2:
            self.camera_y += y

        if self.collision(0,y,0,units):
           y= 0
        
        
        
        match [x//2.5,y//2.5]: # match the rotation to the movement
          case [1,0]: # right
            self.rotation_target = 90
          case [-1,0]:
            self.rotation_target = 270
          case [1,1]:
              self.rotation_target = 45
          case [-1,-1]:
              self.rotation_target = 225
          case [1,-1]:
              self.rotation_target = 135
          case [-1,1]:
              self.rotation_target = 315
          case [0,1]:
              self.rotation_target = 0
          case [0,-1]:
              self.rotation_target = 180
        # print(self.rotation, self.rotation_target)
        if self.rotation <= 0: # handle overflows
           self.rotation = 360 - self.rotation
        elif self.rotation > 360:
           self.rotation = self.rotation - 360

        if self.rotation_target != self.prev_case:
          self.difference = (self.rotation_target - self.rotation) % 360 # get initial difference
          
          if self.difference > 180 :
            self.difference = -((360 - self.difference)% 360) # move the scale to 180 / -180
          self.difference = -self.difference #invert the differences so that i can see how much is remaining
        if self.difference < 0: # if the inverted difference is below zero, (or if the original delta angle was positive), move clockwise
           self.difference += 5
           self.rotate(5)
        elif self.difference > 0:# if the inverted difference is above zero, (or if the original delta angle was negative), move counter clockwise
          self.difference -= 5
          self.rotate(-5)
        
        self.prev_case = self.rotation_target

    def collision(self,x,y,axis,units: list[Enemy]):
      """Uses the in range list generated by the thread to check for nearby wall collisions
      Gets rid of wall clipping
      """
      collide = False
      for [x,y] in self.in_range:
        n_x = x*70
        n_y = y*70
        
        # if i need optimizations i can create the rect in the thread
        collider = pg.Rect(n_x-self.camera_x+self.DISPLAY_BASE/2,n_y-self.camera_y+self.DISPLAY_HEIGHT//2,70,70)

        if collider.colliderect(self.bounding_box):
           collide = True
           if axis == 0:
            if collider.top < self.bounding_box.bottom and self.bounding_box.top > collider.top:
                # sets the right edge to edge of left wall. done this way to eliminate clipping
               self.camera_y = n_y +70+ self.height//2
               
            elif collider.bottom > self.bounding_box.top:
               self.camera_y = n_y - self.height//2
               
           else:
              if collider.right > self.bounding_box.left and self.bounding_box.right > collider.right: # put like and other side must be too or smt
                 self.camera_x = n_x+70+ self.width//2
              elif collider.left < self.bounding_box.right:
                 self.camera_x = n_x- self.width//2
        
      for unit in units:
          n_x = unit.x  + unit.offset
          n_y = unit.y + unit.offset
          #print(unit.y, unit.x)

          collider = pg.Rect(n_x-self.camera_x+self.DISPLAY_BASE/2,n_y-self.camera_y+self.DISPLAY_HEIGHT//2,unit.width,unit.height)
          if collider.colliderect(self.bounding_box):
           collide = True
           if axis == 0:
            if collider.top < self.bounding_box.bottom and self.bounding_box.top > collider.top:
                # sets the right edge to edge of left wall. done this way to eliminate clipping
               self.camera_y = n_y +collider.height+ self.height//2
               
            elif collider.bottom > self.bounding_box.top:
               self.camera_y = n_y - self.height//2
               
           else:
              if collider.right > self.bounding_box.left and self.bounding_box.right > collider.right: # put like and other side must be too or smt
                 self.camera_x = n_x+collider.width+ self.width//2
              elif collider.left < self.bounding_box.right:
                 self.camera_x = n_x- self.width//2
      if collide:
         return True
      else:
         return False

    def rotate(self, rotate):
        """Rotates the player image (not hitbox) by 'rotate' degrees"""
        old_centre = self.rect.center
        self.rotation += rotate
        self.image = pg.transform.rotate(self.image_orig, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = old_centre  


    def get_in_range_walls(self,walls:Walls):
        """Uses a thread to get all walls which are near to the player so that the main thread can run less checks"""
        while self.is_alive:
          
          temp_in_range = []
          for i, [x,y] in enumerate(walls.walls):
            real_x = x*70 + 35 # just making new variable to not need to deal with inheritance
            real_y = y*70 + 35
            if (self.camera_x -50 < real_x + 35 < self.camera_x+50 or self.camera_x -50 < real_x - 35 < self.camera_x+50) and (self.camera_y -50 < real_y + 35 < self.camera_y+50 or self.camera_y -50 < real_y - 35 < self.camera_y+50):
                temp_in_range.append([x,y])
          self.in_range = [x for x in temp_in_range]
          # print(self.in_range)
          time.sleep(0.01)


def Create_Container(player):
  """Creates a container which wraps the player for render. \nInput : object of class Player.\nOutput : pg.sprite.Group() object containing player object"""
  player_list = pg.sprite.Group()
  player_list.add(player)
  player_list.add(player.turret)
  return player_list
