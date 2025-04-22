# make a tkinter style ui library for the gui
# except keep pygame style limitations as defining positions because I'm not coding a full packing

import pygame as pg
from typing import NewType
from collections import defaultdict
from ..utils.display.colours import *

class Window:
    """Window class. Fix up definition later. will use pack system like tkinters"""
    transparency_key = BLACK
    def __init__(self, width:int, height:int, transparency_key: tuple[int] = BLACK):


        self.__width = width
        self.__height = height
        self.__surf = pg.Surface([self.__width, self.__height])
        self.__surf.set_colorkey(transparency_key)
        self.__surf.fill(transparency_key)

        self.__collidables: dict[objectID, pg.Rect] = defaultdict()
        self.__objects: dict[objectID, Object] = defaultdict()
        # objects are held in __objects for recalculations based on hover and data status
        # object rects are held in __collidables for mouse collision purposes

    def pack(self, object, position: tuple[float]=(0,0), dimensions: tuple[int]=(0,0),ID = None) -> None:

        if ID is None: # add a identity creation func
            ID = __create_id(object)
        
        if object == "grid":
            self.__gridhandler(object, position)
        else:
            object: Object = object

            self.__surf.blit(object.image,position)

            self.__objects[ID] = object
            self.__collidables[ID] = pg.Rect(
                position[0], 
                position[1],
                dimensions[0],
                dimensions[1]
            )

    

    def __gridhandler(self, grid, position):
        """Private method whichs handles .pack operations for all subitems of a grid"""
        grid:Grid = grid
        
        for identity in grid._objects:
            identity:objectID

            object, (column_position, row_position, column_span) = grid._objects[identity]
            x = position[0] + column_position * grid._column_width
            y = position[1] + row_position * grid._row_height
            self.pack(object,(x,y), (grid._column_width*column_span, grid._row_height), identity)



class Grid:
    """Grid class. will work similary to tkinter grid"""
    def __init__(self, window:Window, columns:int=1, rows:int=1, columnwidth:float = 10, rowheight:float = 10):
        # if an object doesn't fit in its defined grid space crop it

        self._column_count = columns
        self._row_count = rows
        self._column_width = columnwidth
        self._row_height = rowheight
        # work on everything else next then come back to this

        self._objects:dict[objectID, list] = {}
        # list is defined as [object, (col_pos, row_pos, span)]

    def __eq__(self,other):
        return other == "grid"

    def __str__(self):
        return "grid"
    

class Object:
    """Default object class which all sub-objects like buttons inherit from"""

    def __init__(self):
        self.image = pg.Surface([0,0])
        self.value = None

    def __str__(self):
        return "object"



__past_ids = []
def __create_id(object) -> str:
    """Given an object inherited from the Object class, returns a unique id"""
    id_suffix = 0
    object_type = str(object)
    while (id := object_type+str(id_suffix)) in __past_ids: 
        id_suffix += 1
    __past_ids.append(id)
    return id
        

# define custom types
objectID = NewType('objectID', str)
objectRect = NewType('objectRect', list[float])
grid = NewType('grid', Grid)


if __name__ == "__main__":
    # for testing
    BLACK = (0, 0, 0)
    Obj = Object()