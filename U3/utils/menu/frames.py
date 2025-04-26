import pygame as pg
from ..display.colours import *
from lib.pymenu import pymenu as mu

def create_frames(window:mu.Window):
    """Creates all frames used in the game"""

    # starting frame INCOMPLETE

    background = mu.Background(window, width=200, height=200, border_width=3, corner_radius=2,background_color=BLACK,border_color=BLACK,alpha=160)
    window.pack(background, (0,0), ID="background")

    grid = mu.Grid(columns=1, rows=1, columnwidth=100,rowheight=100)

    label = mu.Label(window, "Just a test", width=100, text_size=15, border_width=3, corner_radius=2)
    grid.pack(label, row=0, column=0, columnspan=1, ID="Test")

    window.pack(grid, (0,0))
    window.save_frame("start",flush=True)