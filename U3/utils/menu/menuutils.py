import pygame as pg




class Grid:
    
    def __init__(self, position: tuple[int]=(0,0), columns=1, rows=1, columnwidth = 10, rowheight = 10):
        self.x = position[0]
        self.y = position[1]

        self.column_count = columns
        self.row_count = rows
        self.column_width = columnwidth
        self.row_height = rowheight
        

Grid()