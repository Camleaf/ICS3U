from dataclasses import dataclass, field
from typing import Any
import pygame as pg
from ..display.colours import *
import time, heapq, math

class Enemy:
    """The individual class for each enemy"""
    def __init__(self, color, width, height, posx, posy, DISPLAY_HEIGHT, DISPLAY_BASE, GAME_BASE, GAME_HEIGHT, camera_x, camera_y):
        self.image_orig = pg.Surface([width,height])
        self.image_orig.set_colorkey((255,255,255))
        self.image_orig.fill(color)
        pg.draw.rect(self.image_orig,OFF_YELLOW,(0,height-height/9,width,height/9))
        pg.draw.rect(self.image_orig,OFF_YELLOW,(width/9,0,width/7,height))
        pg.draw.rect(self.image_orig,OFF_YELLOW,(width-width/9-width/7,0,width/7,height))


        self.x = posx
        self.y = posy
        self.camera_x = camera_x
        self.camera_y = camera_y
        self.is_alive = True
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.center = [posx-DISPLAY_BASE//2+GAME_BASE//2, posy-DISPLAY_HEIGHT//2+GAME_HEIGHT//2] # this is just initial we change it later
        self.rotation = 0


    def pathfind(self,lock,maze):
        """A thread which continually runs the a-star algorithm to get the path towards the player"""
        while self.is_alive:
            with lock: # we only want one pathfinding algorithm to run at a time given the insane processing overhead, even dealing with multiple threads
                
                # code 8 way dijkstra with exclusion 
                start_node = Tile(None, (self.x//70,self.y//70), 0, 0)
                end_node = (self.camera_x//70, self.camera_y//70)
                visited = [[False for i in range(len(maze[0]))] for _ in range(len(maze))]




                heap = [] # list of tiles
                heapq.heappush(heap, start_node)
                
                self.path = self.a_star(visited,end_node,heap, maze, start_node)

                
            time.sleep(0.5)


    def move(self):
        ...

    def rotate(self, rotate):
        """Rotates the enemy image (not hitbox) by 'rotate' degrees"""
        self.rotation += rotate
        self.image = pg.transform.rotate(self.image_orig, self.rotation)

    def a_star(self,visited,end_node,heap, maze, start_node):
        """A star algorithm modified for the grid used in this projects"""

        # once bullets get introduced I can just temporarily modify the maze in each cycle to have bullets as the maze. Then the bots will pathfind away from bullets
        while heap:
            current_tile:Tile = heapq.heappop(heap) # because of heap object we always have lowest cost


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
                heuristic = round(math.sqrt(((child_position[0] - end_node[0]) ** 2) + ((child_position[1] - end_node[1]) ** 2)))
                
                cost = dist_from_start + heuristic

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
                heuristic = round(math.sqrt(((child_position[0] - end_node[0]) ** 2) + ((child_position[1] - end_node[1]) ** 2)))
                
                cost = dist_from_start + heuristic

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
        
