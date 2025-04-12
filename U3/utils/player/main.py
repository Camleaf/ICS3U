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

      self.image = pg.Surface([width,height])
      self.image.fill(color)

      self.rect = self.image.get_rect()
      self.rect.center = (DISPLAY_BASE/2, DISPLAY_HEIGHT/2)

      self.xpos = GAME_BASE/2
      self.ypos = GAME_HEIGHT / 2
      
      self.speed = 0

    def move(self, speed, rotate):
       ...




def Create_Player(player):
  player_list = pg.sprite.Group()
  player_list.add(player)
  return player_list