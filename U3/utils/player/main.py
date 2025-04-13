import pygame as pg
import math

class Player(pg.sprite.Sprite):
    """The player. Contains functions
      - __init__ | initializes the function
      - move | moves the player
    """
    image: pg.Surface
    xpos: float
    ypos: float
    speed: float

    def __init__(self,color, width:int, height:int, DISPLAY_BASE:int, DISPLAY_HEIGHT:int, GAME_BASE:int, GAME_HEIGHT:int):
      pg.sprite.Sprite.__init__(self)



      # image origin
      self.image_orig = pg.Surface([width,height])
      self.image_orig.set_colorkey((255,255,255))
      self.image_orig.fill(color)
      self.image = self.image_orig.copy()
      self.rect = self.image.get_rect()
      self.rect.center = (DISPLAY_BASE/2, DISPLAY_HEIGHT/2)

      self.width = width
      self.height = height
      self.GAME_BASE = GAME_BASE
      self.GAME_HEIGHT = GAME_HEIGHT
      self.rotation = 180
      self.camera_x = GAME_BASE/2
      self.camera_y = GAME_HEIGHT / 2
      self.rotation_target = 180
      self.speed = 0
      self.prev_case = 180
      self.difference = 0

    def move(self, x, y):
        # print(x,y, self.camera_x, self.camera_y) # debugging
        # all this movement code is temporary and for testinguntil i have a good enough base to go do rotation stuff
        if self.width/2 < self.camera_x + x < self.GAME_BASE - self.width/2:
          self.camera_x += x

        if self.height/2 < self.camera_y + y < self.GAME_HEIGHT - self.height/2:
          self.camera_y += y
        
        
        match [x//2,y//2]: # match the rotation to the movement
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

        
    def rotate(self, rotate):
        """Rotates the player image (not hitbox) by 'rotate' degrees"""
        old_centre = self.rect.center
        self.rotation += rotate
        self.image = pg.transform.rotate(self.image_orig, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = old_centre  

def Create_Container(player):
  """Creates a container which wraps the player for render. \nInput : object of class Player.\nOutput : pg.sprite.Group() object containing player object"""
  player_list = pg.sprite.Group()
  player_list.add(player)
  return player_list
