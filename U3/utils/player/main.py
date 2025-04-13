import pygame as pg

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
      self.rotation = 0
      self.camera_x = GAME_BASE/2
      self.camera_y = GAME_HEIGHT / 2
      
      self.speed = 0

    def move(self, x, y):
        # print(x,y, self.camera_x, self.camera_y) # debugging
        # all this movement code is temporary and for testinguntil i have a good enough base to go do rotation stuff
        if self.width/2 < self.camera_x + x < self.GAME_BASE - self.width/2:
          self.camera_x += x

        if self.height/2 < self.camera_y + y < self.GAME_HEIGHT - self.height/2:
          self.camera_y += y
           


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
