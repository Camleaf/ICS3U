# Pygame-Menu

### These docs are very incomplete and I am doing them in the order that I feel like so It may skip around a lot
## License

## How to use
### Step by Step
#### 1. Download Pygame-Menu.py
Download the repo zip file or the python file
#### 2. Add to lib folder
Extract/move the file into the working directory `/lib` folder
#### 3. Install Pygame-ce
If normal pygame is installed, run `pip3 uninstall pygame`
Then run `pip3 install pygame-ce`; pygame-ce is faster, backwards compatible with regular python projects, and is required for this library.
#### 4. Import into code
In the file while you want to use the library paste this:
```python
import lib.pygame_menu as mu
```

## Lib Classes

###  Window Class

#### Methods
- `pack(self, object, position: tuple[float]=(0,0), dimensions: tuple[int]=(0,0),ID = None) -> None:`
- `set_font_file`
- `set_placeholder_file`
- `__gridhandler`
- `mouseInteraction`
- `keyboardInteraction`
- `update_surf`
- `update_stat`
- `return_state`
- `save_frame`
- `load_frame`
- `flush`
- `create_link()`
- `surface`


## Making your own pygame_menu object classes
### Makeup of an Object
You may have seen the __Object referenced more than once in the previous description, but what does it represent?

```python
class __Object:

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

    def render(self) -> None:
        ...

    def __str__(self):
        return "object"    
        
```

The `__Object` class is an empty shell; It is the datastructure which the organizational classes such as `Window` and `Grid` interpret other objects which have different respective ways of operating. 




So `__Object` provides the structure for every other class to inherit from; The render function on the `__Object` is empty as thay it meant to be replaced and interpreted by the classes which inherit from it.

Since almost all the main objects in the library inherit from this class, at the start it contains every variable used by `window`. Not all of these, `activated, _func, _args, text, image_path` will be used in each module, and as such they always should be passed none when inheriting.

The `self.type` is what gives the Window class more information on what kind of object this is. `label` means that the object is static, `func` means it contains a function that can be activated on interaction, `textbox` means it can be interacted with via keyboard, and `val` means it can simply activate and deactivate.

To show how this is a shell, take the relatively simple `Background` class:
```python
class Background(__Object):
```
It inherits from the __Object, and overwrites everything that the `__Object` doesn't do, like the render function
```python
    def render(self):
        self._image = pg.Surface([self.width,self.height],pg.SRCALPHA)
        self._image.fill((0,0,0,0))
        temp_surf = self._image.copy()

        border_color = [x for x in self.border_color] + [self.alpha]
        background_color = [x for x in self.background_color] + [self.alpha]

        pg.draw.rect(
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
```

Here is the full class:
```python
class Background(__Object):
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
        temp_surf = self._image.copy()

        border_color = [x for x in self.border_color] + [self.alpha]
        background_color = [x for x in self.background_color] + [self.alpha]

        pg.draw.rect(
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
```
The background class would automatically be given a type of `label`, though that can also be manually overwritten if the need arises. The class also does not make use of the `image path, activated, _func, _args, text` default variables, though many other classes do.