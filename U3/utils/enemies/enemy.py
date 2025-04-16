from dataclasses import dataclass, field
from typing import Any, Self
import pygame as pg
from ..display.colours import *
import sys, heapq, math, copy, threading, numpy, time

class Enemy:
    """The individual class for each enemy"""
    def __init__(self, color, width, height, posx, posy, DISPLAY_HEIGHT, DISPLAY_BASE, GAME_BASE, GAME_HEIGHT, camera_x, camera_y, grid, offset, identity):
        self.image_orig = pg.Surface([width,height])
        self.image_orig.set_colorkey((255,255,255))
        self.image_orig.fill(color)
        pg.draw.rect(self.image_orig,OFF_YELLOW,(0,height-height/9,width,height/9))
        pg.draw.rect(self.image_orig,OFF_YELLOW,(width/9,0,width/7,height))
        pg.draw.rect(self.image_orig,OFF_YELLOW,(width-width/9-width/7,0,width/7,height))


        self.x = posx
        self.y = posy
        self.xs = 0
        self.ys= 0
        self.offset = offset
        self.width = width
        self.height = height
        self.camera_x = camera_x
        self.camera_y = camera_y
        self.is_alive = True
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        # self.rect.center = [posx-camera_x+DISPLAY_BASE//2+self.offset, posy-camera_y+DISPLAY_HEIGHT//2+self.offset] # this is just initial we change it later
        self.rotation_target = 180
        self.rotation = 180
        self.prev_case = 180
        self.difference = 0
        self.collision_count = 0
        self.path = []
        self.activated = False
        self.pathfinding_active = False
        self.cur_move_target = (self.x,self.y)
        self.grid = copy.deepcopy(grid)
        self.id = identity
        self.rot_offset = 0


    def pathfind(self,maze):
        """A thread which continually runs the a-star algorithm to get the path towards the player"""
            

        start_node = Tile(None, (int(self.x//70),int(self.y//70)), 0, 0)
        end_node = (int(self.camera_x//70), int(self.camera_y//70))
        visited = [[False for i in range(len(maze[0]))] for _ in range(len(maze))]

        estimation = abs(start_node.position[0]-end_node[0]) + abs(start_node.position[1]-end_node[0]) # uses taxicab dist
        

        if not self.activated:
            if estimation <= 11:
                self.activated = True
            self.pathfinding_active = False
            self.path = []
            return 

        if start_node.position == end_node:
            self.pathfinding_active = False
            self.path = []
            return

        heap = [] # list of tiles
        heapq.heappush(heap, start_node)
        self.path = self.a_star(visited,end_node,heap, maze, start_node)[1:]
        if len(self.path) < 3:# this happening after the search could be a problem
            self.path = []
            time.sleep(0.3)
        
        self.pathfinding_active = False
        sys.exit()


    def move(self, units):
        print(self.id)
        #print(self.cur_move_target, (self.x, self.y), (self.camera_x, self.camera_y))
        if (self.x, self.y) == self.cur_move_target or self.collision_count > 50: #using this to fix the always stuck issue results in a few going through walls issues
            # so f
            self.collision_count = 0
            # pathfinding only really needs to be active when triggered, and in this case the trigger is needing a new move target
            self.recalculate_path()
            if len(self.path) == 0: return
            self.cur_move_target = self.path.pop(0)
            self.cur_move_target = (self.cur_move_target[0] * 70, self.cur_move_target[1] * 70)
        


        self.xs = 0
        
        if self.cur_move_target[0] < self.x:
            self.xs = -2
        elif self.cur_move_target[0] > self.x:
            self.xs = 2

        self.collision(units, self.xs, 0, 0)

        self.ys = 0
        if self.cur_move_target[1] < self.y:
            self.ys = -2
        elif self.cur_move_target[1] > self.y:
            self.ys = 2

        self.collision(units, 0, self.ys, 1)
        
        
        self.rotation_manager(self.xs,self.ys)
    
    def recalculate_path(self):
        """Recalculates pathfinding path by starting a daemon thread of the pathfind() func"""
        if not self.pathfinding_active:
            self.pathfinding_active = True
            r = threading.Thread(target = self.pathfind, args = (copy.deepcopy(self.grid),))
            r.daemon = True
            r.start()

    def collision(self, units:list[Self] , x, y, axis):
        """Checks for collisions with walls or with other bots"""
        col_check = False
        
        if self.grid[int((self.y+y+self.offset)//70)][int((self.x+x+self.offset)//70)] == 1 or self.grid[int((self.y+y+self.offset+self.height)//70)][int((self.x+x+self.offset+self.width)//70)] == 1:
            
            self.collision_count += 1
            col_check = True
            return

        for i, unit in enumerate(units): # now i just need to extend to the player
            if i == self.id: continue
            n_x = unit.x
            n_y = unit.y
            

            t_top = n_y
            t_bottom = n_y + self.height 
            t_left = n_x 
            t_right = n_x + self.width

            s_top = self.y + y
            s_bottom = self.y + self.height + y
            s_left = self.x + x
            s_right = self.x + self.width + x


            if t_right >= s_left and t_left <= s_right and t_bottom >= s_top and t_top <= s_bottom: # check for collision using the rectangle formula
                col_check = True
                break
        if col_check:
            self.collision_count += 1
        else:
            self.x += x
            self.y += y


    def rotation_manager(self,x,y):
        """Gives a rotation target for the bot to match based on its current movement"""
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
        """Rotates the enemy image (not hitbox) by 'rotate' degrees"""
        self.rotation += rotate
        self.image = pg.transform.rotate(self.image_orig, self.rotation)
        self.rot_offset = 7.5 - abs((((self.rotation % 90) / 45) -1) * 7.5)

    def a_star(self,visited,end_node,heap, maze, start_node):
        """A star algorithm modified for the grid used in this projects"""
        # once bullets get introduced I can just temporarily modify the maze in each cycle to have bullets as the maze. Then the bots will pathfind away from bullets
        # so the astar breaks whenever the player goes past or equal to 10 on x or y axis
        #    update: start node is fine. end node is fine. all the passed inputs are fine WHAT THE HELL IS HAPPENING
        #    update: i fixed it the issue was I swapped game height/bsae with display height/base :facepalm:
        rng = numpy.random.default_rng()
        while heap:
            current_tile:Tile = heapq.heappop(heap) # because of heap object we always have lowest cost
            visited[current_tile.position[1]][current_tile.position[0]] = True

            if current_tile.position == end_node:
                path = []
                current = current_tile
                while current:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]

            # create children of current node
            for vector in ((1,0),(-1,0),(0,1),(0,-1)): # horizontal vectors
                
                child_position = (
                    current_tile.position[0]+vector[0], # x
                    current_tile.position[1]+vector[1]  # y
                )
                # print()
                # print(end_node, current_tile.position, child_position)
                if not 0 <= child_position[0] < len(maze[0]) or not 0 <= child_position[1] < len(maze):
                    # check for out of bounds
                    continue

                if maze[child_position[1]][child_position[0]] == 1:
                    # check if wall in new position
                    continue
                
                if visited[child_position[1]][child_position[0]]:
                    # check if already seen
                    continue
            
                dist_from_start = current_tile.dist + 1

                # pythagorean theorem
                heuristic = int(round(math.sqrt(((child_position[0] - end_node[0]) ** 2) + ((child_position[1] - end_node[1]) ** 2))))
                
                cost = dist_from_start + heuristic + rng.integers(0,3,1)

                heapq.heappush(heap,Tile(current_tile, child_position, dist_from_start, cost))

            # diagonals
            for vector in ((1,1),(-1,-1),(1,-1),(-1,1)):
                child_position = (
                    current_tile.position[0]+vector[0], # x
                    current_tile.position[1]+vector[1]  # y
                )
                if not 0 <= child_position[0] < len(maze[0]) or not 0 <= child_position[1] < len(maze):
                    # check for out of bounds
                    continue

                if maze[child_position[1]][child_position[0]] == 1:
                    # check if wall in new position
                    continue
                
                if visited[child_position[1]][child_position[0]]:
                    # check if already seen
                    continue

                if maze[child_position[1]][current_tile.position[0]] == 1 or  maze[current_tile.position[1]][child_position[0]] == 1:
                    continue

                dist_from_start = current_tile.dist + 1

                # pythagorean theorem
                heuristic = int(round(math.sqrt(((child_position[0] - end_node[0]) ** 2) + ((child_position[1] - end_node[1]) ** 2))))
                
                cost = dist_from_start + heuristic + rng.integers(0,3,1)
                heapq.heappush(heap,Tile(current_tile, child_position, dist_from_start, cost))


        return [start_node.position]
            
            

    def player_pass(self,camera_x,camera_y):
        """Passes camera_x and camera_y to the local class so that the pathfinding thread can use it"""
        self.camera_x = camera_x
        self.camera_y = camera_y

@dataclass(order=True)
class Tile:
    """A tile for the elements in the pathfind algorithm"""
    # field compare false just makes it not in the way when trying to compare the classes in heapq
    parent: Any=field(compare=False)
    position: Any=field(compare=False)
    dist: int=field(compare=False)
    cost: int
        
