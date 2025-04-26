import pygame as pg
from ..display.colours import *
from lib.pymenu import pymenu as mu

import os

def create_frames(window:mu.Window, menu, GAME_BASE,GAME_HEIGHT):
    """Creates all frames used in the game"""
    # ingame screen


    window.save_frame("ingame",flush=True)



    # Welcome Screen

    background = mu.Background(window, width=GAME_BASE, height=GAME_HEIGHT, border_width=3, corner_radius=2,background_color=BLACK,border_color=BLACK,alpha=100)
    window.pack(background, (0,0))

    background = mu.Background(window, width=500, height=400, border_width=6, corner_radius=10,background_color=VERY_DARK_PICKLE_GREEN,border_color=OFF_GREY,alpha=255)
    window.pack(background, (100,150))

    grid = mu.Grid(columns=10, rows=10, columnwidth=50,rowheight=50)

    window.set_font_file(os.path.join(f'{os.getcwd()}','assets','titleFont.ttf')) # switch to title font for the title

    label = mu.Label(window, "VERY COOL TANKS", width=1000, text_size=60, text_color=LIGHT_ORANGE,background_alpha=0)
    grid.pack(label, row=0, column=1, columnspan=8, ID="Title")

    window.set_font_file(os.path.join(f'{os.getcwd()}','assets','gameFont.ttf'))

    label = mu.Label(window, "Welcome!", width=200, text_size=40, border_width=0, text_color=LIGHT_ORANGE, background_alpha=0)
    grid.pack(label, row=2, column=3, columnspan=8, ID="WelcomeLabel")

    label = mu.Label(window, 
'''This game is a tanks game. That means that you try to survive against an onslaught of enemy tanks. One shot is enough to destroy your tank. Good luck\n\nControls: \n    W - up, S - down, A - left, D - right, \n    Mouse - aim, Space - shoot\n\n''', 
                    width=400,
                    text_size=20,
                    text_color=LIGHT_ORANGE,
                    background_alpha=0
    )
    grid.pack(label,row=4,column=1,columnspan=8, ID="DescriptionText")

    button = mu.Button(window, "Continue", command=menu.switch_frame, args=("main",), width=-1, text_size=25, border_width=3, corner_radius=2, border_color=OFF_GREY, background_color=LIGHT_ORANGE, text_color=VERY_DARK_PICKLE_GREEN)
    window.pack(button, (299,475), ID="ContinueButton") # I did this one manually because of the custom width fit


    window.pack(grid, (100,50))
    window.save_frame("welcome",flush=True)




    ### Main Menu

    background = mu.Background(window, width=GAME_BASE, height=GAME_HEIGHT, border_width=3, corner_radius=2,background_color=BLACK,border_color=BLACK,alpha=100)
    window.pack(background, (0,0))

    background = mu.Background(window, width=500, height=400, border_width=6, corner_radius=10,background_color=VERY_DARK_PICKLE_GREEN,border_color=OFF_GREY,alpha=255)
    window.pack(background, (100,150))

    grid = mu.Grid(columns=10, rows=10, columnwidth=50,rowheight=50)
    
    button = mu.Button(window, "Play", command=menu.enter_game, args=tuple(), width=-1, text_size=25, border_width=3, corner_radius=2, border_color=OFF_GREY, background_color=LIGHT_ORANGE, text_color=VERY_DARK_PICKLE_GREEN)
    window.pack(button, (327,475), ID="Playbutton")


    window.pack(grid, (100,50))
    window.save_frame("main", flush=True)