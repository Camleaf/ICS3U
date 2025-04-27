"""
The pygame menu library that I made just for a school tanks game

Dependencies: 
- Python >= 3.11.9
- Pygame >= 2.2.6
"""
import pygame as pg
from typing import NewType
from typing import Any
from copy import deepcopy
import os

# default color declarations just since it is a library
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (100,100,100)
BLUE = (0,0,255)

class Empty:
    ...

class Window:
    """Window class. Fix up definition later. will use pack system like tkinters"""
    def __init__(self, width:int, height:int, transparency_key: tuple[int] = BLACK):
        
        self.transparency_key = transparency_key

        self._default_font_file = os.path.join(f"{os.getcwd()}","gameFont.ttf")
        self.__width = width
        self.__height = height
        self.__surf = pg.Surface([self.__width, self.__height],pg.SRCALPHA)
        self.__surf.fill((0,0,0,0))

        self.__collidables: dict[objectID, pg.Rect] = {}
        self._objects: dict[objectID, __Object] = {}
        self.__frames: dict[objectID, Any] = {}
        # objects are held in _objects for recalculations based on hover and data status
        # object rects are held in __collidables for mouse collision purposes

    def pack(self, object, position: tuple[float]=(0,0), dimensions: tuple[int]=(0,0),ID = None) -> None:
        """Assign the object to the current frame"""
        
        if object == "grid":
            self.__gridhandler(object, position)
        else:
            if ID is None: # add a identity creation func
                ID = _create_id(object)
            object: __Object = object

            self._objects[ID] = object
            if dimensions != (0,0): # if dimensions are given use them
                self.__collidables[ID] = pg.Rect(
                    position[0], 
                    position[1],
                    dimensions[0],
                    dimensions[1]
                )
            else: # otherwise use the rect of the image
                self.__collidables[ID] = object._image.get_rect()
                self.__collidables[ID].topleft = position
            self.update_surf(ID)
    
    
    def set_font_file(self, file_path):
        self._default_font_file = file_path
    
    def __gridhandler(self, grid, position):
        """Private method whichs handles .pack operations for all subitems of a grid"""
        grid:Grid = grid
        
        for identity in grid._objects:
            identity:objectID

            # create positions based off the grid position and the row and column position
            object, (column_position, row_position, column_span) = grid._objects[identity]
            x = position[0] + column_position * grid._column_width
            y = position[1] + row_position * grid._row_height
            self.pack(object,(x,y), ID=identity)

    def mouseInteraction(self, position):
        """Function which handles all mouseclick"""
        for ID in self.__collidables:
            object = self._objects[ID]
            collidable = self.__collidables[ID]
            
            if object.type == "label": continue

            if not collidable.collidepoint(position[0],position[1]):

                if object.type == "textbox": 
                    object.activated = False
                    self.update_surf(ID)

                continue
            
            if object.type == "func":
                ret = self._objects[ID]._func(*self._objects[ID]._args)
                if not ret and ret is not None: # if the function returns false, it means it should not update the surface, however if it is none it should by default update
                    return
            elif object.type == "val":
                self._objects[ID].activated = True if not self._objects[ID].activated else False
            elif object.type == "textbox":
                self._objects[ID].activated = True
                self._objects[ID].cursor_pos = len(object.text)-1
            self.update_surf(ID)

            

    def keyboardInteraction(self, key):
        """Function which handles all keyboard interactions with objects"""

        for ID in self._objects:
            object = self._objects[ID]
            if object.type != "textbox": continue
            if not object.activated: continue

            new_text = object.text[:object.cursor_pos+1] + key + object.text[object.cursor_pos+1:]
            if key == "\x08":
                if len(object.text) != 0:
                    self._objects[ID].text = object.text[:object.cursor_pos] + object.text[object.cursor_pos+1:]
                    self._objects[ID].cursor_pos -= 1
            elif key == "\r":
                self._objects[ID].activated = False
            elif key == "lspr":
                self._objects[ID].cursor_pos -= 1
                if self._objects[ID].cursor_pos != 0:
                    self._objects[ID].cursor_pos %= len(object.text)
            elif key == "rspr":
                self._objects[ID].cursor_pos += 1
                if self._objects[ID].cursor_pos != 0:
                    self._objects[ID].cursor_pos %= len(object.text)
            elif object.input_type == "num" and key in "1234567890":
                
                self._objects[ID].text = new_text
                self._objects[ID].cursor_pos += len(key)
            elif object.input_type == "all":

                self._objects[ID].text = new_text
                self._objects[ID].cursor_pos += len(key)
            self.update_surf(ID)

    def update_surf(self, ID,bg_color:int=(0,0,0,0)):
        collidable = self.__collidables[ID]
        orig_coords = collidable.topleft
        pg.draw.rect(self.__surf, bg_color, collidable)
        self._objects[ID].render()
        self.__collidables[ID] = self._objects[ID]._image.get_rect()
        self.__collidables[ID].topleft = orig_coords
        self.__surf.blit(self._objects[ID]._image,collidable)
    

    def update_stat(self,ID,activated:bool=None,text:str=None, command=None, args:tuple[Any]=None, image_path:str=None):
        """A function to update all default values that can be stored in Object class. For use by user"""
        if activated is not None:
            self._objects[ID].activated = activated
        if text is not None:
            self._objects[ID].text = text
        if command is not None:
            if not callable(command):
                raise Exception(f"Value {command} is not a callable method. Try removing the brackets from the passed function")
            self._objects[ID]._func = command
        if args is not None:
            self._objects[ID]._args = args
        
        if image_path is not None:
            if '/' in image_path and '\\' in image_path:
                raise Exception(f"Image path {image_path} contains both types of slashes")
            if  '/' in image_path:
                image_path.split('/')
            elif '\\' in image_path:
                image_path.split('\\')
            self._objects[ID].image_path = os.path.join(*image_path)

    def return_state(self, ID:str):
        """Returns the default state vars of the object with a given ID"""
        state_export = Empty()
        object = self._objects[ID]
        state_export.activated = object.activated
        state_export.text = object.text
        state_export.command = object._func
        state_export.args = object._args
        state_export.image_path = object.image_path
        return state_export

    def save_frame(self,ID:str,flush:bool = True):
        """Saves the frame by ID, and has the option to flush the current frame"""

        self.__frames[ID] = { # if inheritance issues show up just put copies on everything
            "collidables" : self.__collidables, #{x:self.__collidables[x] for x in self.__collidables}, 
            "objects" : self._objects, #{x:self._objects[x] for x in self._objects},
            "surface": self.__surf
        }
        if flush:
            self.flush()
            

    def delete_frame(self, ID:str):
        """Deletes frame ID"""
        del self.__frames[ID]

    def load_frame(self,ID:str):
        """Loads frame ID"""
        if ID not in self.__frames:
            raise Exception(f"No frame ID {ID} exists")
        frame = self.__frames[ID]
        self.__collidables = frame['collidables']
        self._objects = frame['objects']
        self.__surf = frame['surface']
        return False


    def flush(self):
        """Flushes the current frame, removing all data from it. Data in stored frames are unaffected."""
        self.__surf = pg.Surface([self.__width, self.__height],pg.SRCALPHA)
        self.__surf.fill((0,0,0,0))

        self.__collidables: dict[objectID, pg.Rect] = {}
        self._objects: dict[objectID, __Object] = {}


    def surface(self):
        return self.__surf
    
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

    def pack(self, object, row:int = 0, column:int = 0, columnspan:int = 1, ID:str=None):
        object:__Object = object
        if object == "grid":
            raise Exception("Grid object attempted to pack other Grid object")

        if row < 0 or row > self._row_count-1 or column < 0 or column > self._column_count-1:
            raise Exception("Row or column greater than defined limit of Grid object")
        
        if columnspan > self._column_count or columnspan < 1:
            raise Exception("Columnspan either greater than number of columns, is zero, or is negative")
        if ID is None:
            ID = _create_id(object)
        self._objects[ID] = [object, (column, row, columnspan)]
        



    def __eq__(self,other):
        return other == "grid"

    def __str__(self):
        return "grid"





def _splice(word,font,width,padding,current_width,word_width,size,lines,current_line):
    for i in range(len(word)-1,0,-1): # iterate over the length of the word to see the best fit for splicing the string
        temp_width = font.get_rect(word[0:i+1], rotation=0, size=size).width
        if temp_width > width-padding*2: continue
        if current_width + temp_width <= width-padding*2:
            lines[current_line].append(word[0:i+1] + ' ')
            word = word[i:]
            if font.get_rect(word, rotation=0, size=size).width > width-padding*2:
                lines.append([])
                current_line += 1
                current_width = 0
                return _splice(word,font,width,padding,current_width,word_width,size,lines,current_line)
            break
    return [lines,current_line,current_width, word]

def _create_multiline_text(window:Window, text:str, padding=10, size=20, width=100, color: tuple[int]=BLACK, font_file=None) -> pg.Surface:
    """Handles creating pygame text objects automatically using pg.freetype"""
    # this won't run very much so the overhead can be greater
    if font_file is None:
        font_file = window._default_font_file
    font = pg.font.Font(font_file,size=size)
    if width == -1:
        width = padding//2
    surf = font.render(text,True, color, wraplength=width- padding//2)
    surf.convert_alpha()
    return surf

class __Object:
    """Default object class which all sub-objects like buttons inherit from"""

    def __init__(self, window, value:bool=None, text:str = '', command=None, args:tuple[Any]=None, image_path:str = ''):
        self._image = pg.Surface([0,0],pg.SRCALPHA)
        self.activated = value
        self._func = command
        self._args = args
        self.text = text
        self.window:Window = window
        self.image_path = image_path

        if value is not None and command is not None:
            raise Exception("Objects can not be defined with both a value and a command")
        elif value is not None:
            self.type = "val"
        elif command is not None:
            self.type = "func"
        else:
            self.type = "label"

    def render(self):
        ...
        # add the color purple when this finishes, as all indiv functions will need their own render func


    def __str__(self):
        return "object"    
        
    


__past_ids = []
def _create_id(object:__Object) -> str:
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

# everything above is for infrastructure, below is usable Objects


class Label(__Object):
    """A label class meant for storing multiline text inheriting from __Object"""
    def __init__(self, window, text:str = '', width:int=100, text_padding:int=8, text_size:int=20, border_width:int=3, corner_radius:int=5, background_color: tuple[int] = WHITE, text_color: tuple[int] = BLACK, border_color:tuple[int] = GRAY, background_alpha:int=255, text_alpha:int=255):
        super().__init__(window, value=None, text=text, command=None, args=None)
        self.window = window
        self._default_font_file = self.window._default_font_file
        self.width = width
        self.text_padding = text_padding
        self.border_width = border_width
        self.corner_radius = corner_radius
        self.background_color = background_color
        self.text_color = text_color
        self.border_color = border_color
        self.text_size = text_size
        self.background_alpha = background_alpha
        self.text_alpha = text_alpha
        
    
    def render(self):
        text_color = [x for x in self.text_color] + [self.text_alpha]
        self.text_surf = _create_multiline_text(self.window, padding=self.text_padding, text=self.text, size=self.text_size, width=self.width, color=text_color, font_file=self._default_font_file)
        # image is absed around self.text_surf plus the text padding needed for the border
        if self.width == -1:
            self.width = self.text_surf.get_rect().width

        self._image = pg.Surface([self.width+self.text_padding*2,self.text_surf.get_rect().height+self.text_padding*2],pg.SRCALPHA)
        self._image.fill((0,0,0,0))

        temp_surf = self._image.copy()
        border_color = [x for x in self.border_color] + [self.background_alpha]
        background_color = [x for x in self.background_color] + [self.background_alpha]


        text_surf_height = self.text_surf.get_rect().height
        pg.draw.rect( # make one slightly bigger
            temp_surf, border_color, 
            (0,0,self.width+self.text_padding*2,text_surf_height+self.text_padding*2),  
            border_radius=self.corner_radius
        )
        pg.draw.rect(
            temp_surf, background_color,
            (self.border_width, self.border_width, self.width+self.text_padding*2-self.border_width*2,text_surf_height+self.text_padding*2-self.border_width*2),
            border_radius = self.corner_radius
        )

        self._image.blit(temp_surf, (0,0))
        self._image.blit(self.text_surf, (self.text_padding,self.text_padding))

    def __str__(self):
        return "label"


class Button(Label):
    """A button which triggers a function onclick"""
    # inherits from label for styling options but also contains command
    def __init__(self, window, text:str = '', command=None, args:tuple[Any]=None, width:int=100, text_padding:int=8, text_size:int=20, border_width:int=3, corner_radius:int=5, background_color: tuple[int] = WHITE, text_color: tuple[int] = BLACK, border_color:tuple[int] = GRAY, background_alpha:int=255, text_alpha:int=255):
        super().__init__(window, text, width, text_padding, text_size, border_width, corner_radius, background_color, text_color, border_color, background_alpha, text_alpha)
        self.activated = False
        self._func = command
        self._args = args
        self.type = "func"
    
    def __str__(self):
        return "button"


class TextBox(__Object):
    """A textbox which the user can type in"""
    def __init__(self, window, text:str = '', width:int=100, max_rows:int=1, text_padding:int=8, text_size:int=20, border_width:int=3, corner_radius:int=5, background_color: tuple[int] = WHITE, text_color: tuple[int] = BLACK, border_color:tuple[int] = GRAY, background_alpha:int=255, text_alpha:int=255):
        super().__init__(window, value=False, text=text, command=None, args=None)
        self._default_font_file = window._default_font_file
        self.width = width
        self.text_padding = text_padding
        self.border_width = border_width
        self.corner_radius = corner_radius
        self.background_color = background_color
        self.text_color = text_color
        self.border_color = border_color
        self.text_size = text_size
        self.background_alpha = background_alpha
        self.text_alpha = text_alpha
        self.max_height = text_size * max_rows + self.text_padding*2
        self.type = "textbox"
        self.input_type = "all"
        self.cursor_pos = len(text)
    
    def render(self):
        text_color = [x for x in self.text_color] + [self.text_alpha]
        cursortext = self.text[:self.cursor_pos+1] + '|' + self.text[self.cursor_pos+1:] if self.activated else self.text
        self.text_surf = _create_multiline_text(self.window, padding=self.text_padding, text=cursortext, size=self.text_size, width=self.width, color=text_color, font_file=self._default_font_file)
        while self.text_surf.height > self.max_height:
            self.text = self.text[:-1]
            self.text_surf = _create_multiline_text(self.window, padding=self.text_padding, text=self.text+'|' if self.activated else self.text, size=self.text_size, width=self.width, color=self.text_color, font_file=self.window._default_font_file)
            
        # image is based around self.text_surf plus the text padding needed for the border
        self._image = pg.Surface([self.width+self.text_padding*2,self.text_surf.get_rect().height+self.text_padding*2],pg.SRCALPHA)
        self._image.fill((0,0,0,0))

        temp_surf = self._image.copy()
        border_color = [x for x in self.border_color] + [self.background_alpha]
        background_color = [x for x in self.background_color] + [self.background_alpha]
        

        text_surf_height = self.text_surf.get_rect().height
        pg.draw.rect( # make one slightly bigger
            temp_surf, border_color, 
            (0,0,self.width+self.text_padding*2,text_surf_height+self.text_padding*2),  
            border_radius=self.corner_radius
        )
        pg.draw.rect(
            temp_surf, background_color,
            (self.border_width, self.border_width, self.width+self.text_padding*2-self.border_width*2,text_surf_height+self.text_padding*2-self.border_width*2),
            border_radius = self.corner_radius
        )

        self._image.blit(temp_surf, (0,0))
        self._image.blit(self.text_surf, (self.text_padding,self.text_padding))

    def __str__(self):
        return "textbox"

class CheckBox(__Object):
    """A box which the user can tick on and off"""
    def __init__(self, window, value:bool=False, width=20, height=20, border_width:int=1, corner_radius:int=10, background_color: tuple[int] = WHITE, on_color: tuple[int] = BLUE, border_color:tuple[int] = GRAY):
        super().__init__(window, value=value)
        self.width = width
        self.height = height
        self.border_width = border_width
        self.corner_radius = corner_radius
        self.background_color = background_color
        self.on_color = on_color
        self.border_color = border_color
        self.type = "val"

    def render(self):

        # redefine image in case of any state changes
        self._image = pg.Surface([self.width,self.height],pg.SRCALPHA)
        self._image.fill((0,0,0,0))

        pg.draw.rect( # make one slightly bigger
            self._image, self.border_color, 
            (0,0,self.width,self.height),  
            border_radius=self.corner_radius
        )
        # switch the color of the check if it is on
        if self.activated:
            pg.draw.rect(
                self._image, self.on_color,
                (self.border_width, self.border_width, self.width-self.border_width*2,self.height-self.border_width*2),
                border_radius = self.corner_radius
            )
        else:
            pg.draw.rect(
                self._image, self.background_color,
                (self.border_width, self.border_width, self.width-self.border_width*2,self.height-self.border_width*2),
                border_radius = self.corner_radius
            )
    
    def __str__(self):
        return "checkbox"

class Background(__Object):
    """Object which only contains colors. Holds an alpha channel"""
    def __init__(self, window, width:int=100, height:int=100, border_width:int=3, corner_radius:int=2, background_color: tuple[int] = WHITE, border_color:tuple[int] = GRAY, alpha:int=255):
        super().__init__(window, value=None, text='', command=None, args=None)
        self.width = width
        self.height = height
        self.alpha = alpha
        self.border_width = border_width
        self.corner_radius = corner_radius
        self.background_color = background_color
        self.border_color = border_color
        
    
    def render(self):
        self._image = pg.Surface([self.width,self.height],pg.SRCALPHA)
        self._image.fill((0,0,0,0))
        # I could do this more efficiently but it's a template for the others where I can't
        temp_surf = self._image.copy()

        border_color = [x for x in self.border_color] + [self.alpha]
        background_color = [x for x in self.background_color] + [self.alpha]

        pg.draw.rect( # make one slightly bigger
            temp_surf, border_color, 
            (0,0,self.width,self.height),  
            border_radius=self.corner_radius
        )
        pg.draw.rect(
            temp_surf, background_color,
            (self.border_width, self.border_width, self.width-self.border_width*2,self.height-self.border_width*2),
            border_radius = self.corner_radius
        )
        
        self._image.blit(temp_surf,(0,0))
    
    def __str__(self):
        return "background"


class Image(__Object):
    """Image class. Hasn't been tested yet but should, in theory, work. CHANGE THIS ONCE TESTED"""
    def __init__(self,window:Window, image_path:str='',width:int=100, height:int=100, border_width:int=0,corner_radius:int=10, border_color: tuple[int] = GRAY, alpha:int=255, border_alpha:int=255):
        # still need to finish this
        ### todo
        super().__init__(window, image_path=image_path)
        self.width = width
        self.height = height
        self.alpha = alpha
        self.border_width =border_width
        self.corner_radius = corner_radius
        self.border_alpha = border_alpha
        self.border_color = border_color
        self.type="label"
    
    def render(self):
        self._image = pg.Surface([self.width,self.height],pg.SRCALPHA)
        self._image.fill((0,0,0,0))


        im_surf = pg.Surface([self.width-self.border_width*2,self.height-self.border_width*2], pg.SRCALPHA)
        im_surf.blit(pg.transform.scale(pg.image.load(self.image_path),[self.width-self.border_width*2,self.height-self.border_width*2]))





        # contineu this later
        img_size = im_surf.get_size()
        rect_img = pg.Surface(img_size,pg.SRCALPHA)
        pg.draw.rect(rect_img, WHITE, (0, 0, *img_size), border_radius=self.corner_radius)

        im_surf.blit(rect_img,(0,0),None, pg.BLEND_RGBA_MIN)

        temp_surf = self._image.copy()
        self._image.blit(im_surf, (0,0))

        border_color = [x for x in self.border_color] + [self.border_alpha]
        if self.border_width > 0:
            pg.draw.rect(temp_surf, border_color, (0,0,*img_size), border_radius=self.corner_radius)
            pg.draw.rect(temp_surf, (0,0,0,0),(self.border_width,self.border_width,img_size[0]-self.border_width*2, img_size[1]-self.border_width*2), border_radius=self.corner_radius)
            #add a alpha in the centre to make a border
            self._image.blit(temp_surf, (0,0))
    
    def __str__(self):
        return "image"