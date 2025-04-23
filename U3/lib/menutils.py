# make a tkinter style ui library for the gui
# two names I'm thinking of: menutils and pykinter
# except keep pygame style limitations as defining positions because I'm not coding a full packing
# no text boxes: I could code them but that would be painful and messy

import pygame as pg
from typing import NewType
from collections import defaultdict
#from ..utils.display.colours import *
from typing import Any
BLACK = (0,0,0)
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

        
        if object == "grid":
            self.__gridhandler(object, position)
        else:
            if ID is None: # add a identity creation func
                ID = __create_id(object)
            object: Object = object
            object.width = dimensions[0]
            object.height = dimensions[1]

            self.__objects[ID] = object
            self.__collidables[ID] = pg.Rect(
                position[0], 
                position[1],
                dimensions[0],
                dimensions[1]
            )
            self.__update(ID)
    
    

    def __gridhandler(self, grid, position):
        """Private method whichs handles .pack operations for all subitems of a grid"""
        grid:Grid = grid
        
        for identity in grid._objects:
            identity:objectID

            object, (column_position, row_position, column_span) = grid._objects[identity]
            x = position[0] + column_position * grid._column_width
            y = position[1] + row_position * grid._row_height
            self.pack(object,(x,y), (grid._column_width*column_span, grid._row_height), identity)

    def mouseInteraction(self, position):
        """Function which handles all mouseclick"""
        for ID in self.__collidables:
            object = self.__objects[ID]
            collidable = self.__collidables[ID]
            if not collidable.collidepoint(position[0],position[1]):

                if object.type == "val": object.activated = False

                continue
            
            if object.type == "func":
                self.__objects[ID]._func(*self.__objects[ID]._args)
            else:
                self.__objects[ID].activated = True
            self.__update(ID)

            

    def keyboardInteractions(self, key):
        """Function which handles all keyboard interactions with objects"""

        for ID in self.__objects:
            object = self.__objects[ID]
            collidable = self.__collidables[ID]
            if object.type == "func": continue

            if not object.activated: continue
            
            self.__objects[ID].text += key
            self.__update(ID)

    def __update(self, ID):
        collidable = self.__collidables[ID]
        self.__objects[ID].render()
        self.__surf.blit(self.__objects[ID]._image,collidable.topleft)
        


class Grid:
    """Grid class. will work similary to tkinter grid"""
    def __init__(self, columns:int=1, rows:int=1, columnwidth:float = 10, rowheight:float = 10):
        # if an object doesn't fit in its defined grid space crop it

        self._column_count = columns
        self._row_count = rows
        self._column_width = columnwidth
        self._row_height = rowheight
        # work on everything else next then come back to this

        self._objects:dict[objectID, list] = {}
        # list is defined as [object, (col_pos, row_pos, span)]

    def pack(self, object, row:int = 0, column:int = 0, columnspan:int = 1):
        object:Object = object
        if object == "grid":
            raise Exception("Grid object attempted to pack other Grid object")

        if row < 0 or row > self._row_count-1 or column < 0 or column > self._column_count-1:
            raise Exception("Row or column greater than defined limit of Grid object")
        
        if columnspan > self._column_count or columnspan < 1:
            raise Exception("Columnspan either greater than number of columns, is zero, or is negative")
        
        ID = __create_id(object)
        self._objects[ID] = [object, (column, row, columnspan)]
        



    def __eq__(self,other):
        return other == "grid"

    def __str__(self):
        return "grid"
    

class Object:
    """Default object class which all sub-objects like buttons inherit from"""

    def __init__(self, value:bool=None, text:str = '', command=None, args:tuple[Any]=None):
        self.width = 0
        self.height = 0
        self._image = pg.Surface([0,0])
        self.activated = value
        self._func = command
        self._args = args
        self.text = text

        if value is not None and command is not None:
            raise Exception("Objects can not be defined with both a value and a command")
        elif value is not None:
            self.type = "val"
        elif command is not None:
            self.type = "func"

    def render(self):
        ...
        # add the color purple when this finishes, as all indiv functions will need their own render func


    def __str__(self):
        return "object"




__past_ids = []
def __create_id(object:Object) -> str:
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
