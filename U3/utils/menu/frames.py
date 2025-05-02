import pygame as pg
from ..display.colours import *
from lib.pygame_menu import pygame_menu as mu

import os

def create_frames(window:mu.Window, menu, GAME_BASE,GAME_HEIGHT):
    """Creates all frames used in the game"""
    # ingame screen
    coords = [10,0]
    for life in range(menu.c.player.max_lives):
        if life < menu.c.player.lives:
            image =  mu.Image(window, image_path=os.path.join(os.getcwd(),'assets','images','Heart.png'),width=20,height=28)
        else:
            image =  mu.Image(window, image_path=os.path.join(os.getcwd(),'assets','Transparent.png'),width=20,height=28)

        window.pack(image, coords, ID="Life"+str(life))
        coords[0] += 30

    window.save_frame("ingame",flush=True)



    ### Welcome Screen

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
    window.pack(button, (294,475), ID="ContinueButton") # I did this one manually because of the custom width fit



    # pack the grid into the frame and then save the frame
    window.pack(grid, (100,50))
    window.save_frame("welcome",flush=True)





    ### Main Menu

    background = mu.Background(window, width=GAME_BASE, height=GAME_HEIGHT, border_width=3, corner_radius=2,background_color=BLACK,border_color=BLACK,alpha=100)
    window.pack(background, (0,0))

    background = mu.Background(window, width=500, height=400, border_width=6, corner_radius=10,background_color=VERY_DARK_PICKLE_GREEN,border_color=OFF_GREY,alpha=255)
    window.pack(background, (100,150))

    grid = mu.Grid(columns=10, rows=10, columnwidth=50,rowheight=50)


    window.set_font_file(os.path.join(f'{os.getcwd()}','assets','titleFont.ttf')) # switch to title font for the title
    label = mu.Label(window, "VERY COOL TANKS", width=1000, text_size=60, text_color=LIGHT_ORANGE,background_alpha=0)
    grid.pack(label, row=0, column=1, columnspan=8, ID="Title")
    window.set_font_file(os.path.join(f'{os.getcwd()}','assets','gameFont.ttf'))


    label = mu.Label(window, "Main Menu", width=300, text_size=40, border_width=0, text_color=LIGHT_ORANGE, background_alpha=0)
    grid.pack(label, row=2, column=3, columnspan=8, ID="WelcomeLabel")


    label = mu.Label(window, 
                    "Difficulty", 
                    text_center='right',
                    width=145,
                    text_size=30,
                    text_color=LIGHT_ORANGE,
                    background_alpha=0
    )
    grid.pack(label,row=3,column=6,columnspan=4, ID="DifficultyLabel")

    label = mu.Label(window, 
                    "Shop",
                    text_center="centre",
                    width=125,
                    text_size=30,
                    text_color=LIGHT_ORANGE,
                    background_alpha=0
    )
    grid.pack(label,row=3,column=1,columnspan=8, ID="ShopLabel")


    button = mu.Button(window, "", text_center="centre",command=menu.set_difficulty, args=(True,), width=25, text_size=30, border_width=3, corner_radius=2, border_color=OFF_GREY, background_color=LIGHT_ORANGE, text_color=VERY_DARK_PICKLE_GREEN)
    window.pack(button, (495,420), ID="DifficultyIncrement") #update this diff to difficulty modify func

    button = mu.Button(window, "", text_center="centre",command=menu.set_difficulty, args=(False,), width=25, text_size=30, border_width=3,corner_radius=2, border_color=OFF_GREY, background_color=LIGHT_ORANGE, text_color=VERY_DARK_PICKLE_GREEN)
    window.pack(button, (445,420), ID="DifficultyDecrement") #update this diff to difficulty modify func
    
    image = mu.Image(window, image_path=os.path.join(os.getcwd(),'assets','images','button', 'bw.png'), width=40, height=40, corner_radius=0)
    window.pack(image, (454,426), ID="DecrementImage")

    image = mu.Image(window, image_path=os.path.join(os.getcwd(),'assets','images','button', 'fw.png'), width=40, height=40, corner_radius=0)
    window.pack(image, (498,426), ID="IncrementImage")

    button = mu.Button(window, "Visit", text_center="centre",command=menu.switch_frame, args=("shop",), width=80, text_size=30, border_width=3, corner_radius=2, border_color=OFF_GREY, background_color=LIGHT_ORANGE, text_color=VERY_DARK_PICKLE_GREEN)
    window.pack(button, (175,420), ID="ShopVisit")

    image = mu.Image(window, image_path=os.path.join(os.getcwd(),'assets','images','Difficulty.png'), width=100, height=140)
    window.pack(image, (439,255), ID="DifficultyImage")

    image = mu.Image(window, image_path=os.path.join(os.getcwd(),'assets','images','Shop.png'), width=100, height=140)
    window.pack(image, (173,255), ID="ShopImage")

    label = mu.Label(window, 
                    "0", 
                    text_center='right',
                    width=80,
                    text_size=16,
                    text_color=LIGHT_ORANGE,
                    border_width=0,
                    background_color=VERY_DARK_PICKLE_GREEN
    )
    window.pack(label, (175,357), ID="GoldNum")

    label = mu.Label(window, 
                    "Civilian", 
                    text_center='centre',
                    width=78,
                    text_size=16,
                    text_color=LIGHT_ORANGE,
                    border_width=0,
                    background_color=VERY_DARK_PICKLE_GREEN
    )
    window.pack(label, (442,357), ID="DifficultyText")
    # still need to create a lot of function

    image = mu.Image(window, image_path=os.path.join(os.getcwd(),'assets','images','Gold.png'),width=20,height=20)
    window.pack(image, (180, 364), ID="GoldImage")
    
    window.create_link("GoldNum", linked_id="GoldImage", backward=False)

    button = mu.Button(window, "Play", command=menu.enter_game, args=tuple(), width=-1, text_size=25, border_width=3, corner_radius=2, border_color=OFF_GREY, background_color=LIGHT_ORANGE, text_color=VERY_DARK_PICKLE_GREEN)
    window.pack(button, (327,485), ID="Playbutton")


    window.pack(grid, (100,50))
    window.save_frame("main", flush=True)






    ### Pause game screen
    
    background = mu.Background(window, width=GAME_BASE, height=GAME_HEIGHT, border_width=3, corner_radius=2,background_color=BLACK,border_color=BLACK,alpha=100)
    window.pack(background, (0,0))


    grid = mu.Grid(columns=10, rows=10, columnwidth=50,rowheight=50)

    window.set_font_file(os.path.join(f'{os.getcwd()}','assets','titleFont.ttf')) # switch to title font for the title
    label = mu.Label(window, "VERY COOL TANKS", width=1000, text_size=60, text_color=LIGHT_ORANGE,background_alpha=0)
    grid.pack(label, row=0, column=1, columnspan=8, ID="Title")
    window.set_font_file(os.path.join(f'{os.getcwd()}','assets','gameFont.ttf'))


    button = mu.Button(window, "Resume Game", command=menu.resume_game, args=tuple(), width=-1, text_size=25, border_width=3, corner_radius=3, border_color=OFF_GREY, background_color=VERY_DARK_PICKLE_GREEN, text_color=LIGHT_ORANGE)
    window.pack(button, (269,250), ID="Playbutton")

    label = mu.Label(window, text="(You will lose any gold gained)", text_center="centre", width=-1, text_size=15, border_width=3, corner_radius=3, text_color=LIGHT_ORANGE, background_alpha=0)
    window.pack(label, (258,400), ID="Menubutton1")

    button = mu.Button(window, "Main Menu", command=menu.menu_exit, args=tuple(), width=-1, text_size=25, border_width=3, corner_radius=3, border_color=OFF_GREY, background_color=VERY_DARK_PICKLE_GREEN, text_color=LIGHT_ORANGE)
    window.pack(button, (288,350), ID="Menubutton")


    window.pack(grid, (100,50))
    window.save_frame("pause", flush=True)



    ### End game

    background = mu.Background(window, width=GAME_BASE, height=GAME_HEIGHT, border_width=3, corner_radius=2,background_color=BLACK,border_color=BLACK,alpha=100)
    window.pack(background, (0,0))


    grid = mu.Grid(columns=10, rows=10, columnwidth=50,rowheight=50)

    window.set_font_file(os.path.join(f'{os.getcwd()}','assets','titleFont.ttf')) # switch to title font for the title
    label = mu.Label(window, "VERY COOL TANKS", width=1000, text_size=60, text_color=LIGHT_ORANGE,background_alpha=0)
    grid.pack(label, row=0, column=1, columnspan=8, ID="Title")
    window.set_font_file(os.path.join(f'{os.getcwd()}','assets','gameFont.ttf'))


    label = mu.Label(window, "VICTORY", width=200, text_size=40, text_color=LIGHT_ORANGE, background_alpha=0, text_center="centre")
    grid.pack(label, row=2, column=3, columnspan=8, ID="StatusLabel")
    label = mu.Label(window, 
                    "Destroying those tanks sure brings a reward...", 
                    text_center='centre',
                    width=200,
                    text_size=16,
                    text_color=LIGHT_ORANGE,
                    border_width=3,
                    background_color=VERY_DARK_PICKLE_GREEN
    )
    window.pack(label, (250,230), ID="DescrText")
    # total gold
    label = mu.Label(window, 
                    "New Total:", 
                    text_center='right',
                    width=85,
                    text_size=16,
                    text_color=LIGHT_ORANGE,
                    border_width=3,
                    background_color=VERY_DARK_PICKLE_GREEN
    )
    window.pack(label, (370,377), ID="GoldTotalText")

    label = mu.Label(window, 
                    "0", 
                    text_center='right',
                    width=85,
                    text_size=16,
                    text_color=LIGHT_ORANGE,
                    border_width=3,
                    background_color=VERY_DARK_PICKLE_GREEN
    )
    window.pack(label, (370,417), ID="GoldNum")

    image = mu.Image(window, image_path=os.path.join(os.getcwd(),'assets','images','Gold.png'),width=20,height=20)
    window.pack(image, (375, 424), ID="GoldImage")
    window.create_link("GoldNum", linked_id="GoldImage", backward=False)
    # gold gained/lost
    label = mu.Label(window, 
                    "You gained", 
                    text_center='right',
                    width=85,
                    text_size=16,
                    text_color=LIGHT_ORANGE,
                    border_width=3,
                    background_color=VERY_DARK_PICKLE_GREEN
    )
    window.pack(label, (245,377), ID="GoldGainedText")
    label = mu.Label(window, 
                    "0", 
                    text_center='right',
                    width=85,
                    text_size=16,
                    text_color=LIGHT_ORANGE,
                    border_width=3,
                    background_color=VERY_DARK_PICKLE_GREEN
    )
    window.pack(label, (245,417), ID="GoldGained")
    #show raw gain/loss
    label = mu.Label(window, 
                    "Gained: 0", 
                    text_center='centre',
                    width=150,
                    text_size=16,
                    text_color=LIGHT_ORANGE,
                    border_width=3,
                    background_color=VERY_DARK_PICKLE_GREEN
    )
    window.pack(label, (275,297), ID="RawGain")

    label = mu.Label(window, 
                    "Repair: 0", 
                    text_center='centre',
                    width=150,
                    text_size=16,
                    text_color=LIGHT_ORANGE,
                    border_width=3,
                    background_color=VERY_DARK_PICKLE_GREEN
    )
    window.pack(label, (275,330), ID="RawRepair")
    # show total gain/loss and total remaining
    image = mu.Image(window, image_path=os.path.join(os.getcwd(),'assets','images','Gold.png'),width=20,height=20)
    window.pack(image, (250, 424), ID="GoldImage2")

    window.create_link("GoldGained", linked_id="GoldImage2", backward=False)

    button = mu.Button(window, "Main Menu", command=menu.menu_exit, args=tuple(), width=-1, text_size=25, border_width=3, corner_radius=3, border_color=OFF_GREY, background_color=VERY_DARK_PICKLE_GREEN, text_color=LIGHT_ORANGE)
    window.pack(button, (288,480), ID="Menubutton")

    window.pack(grid, (100,50))
    window.save_frame("endgame", flush=True)



    ### shop
    background = mu.Background(window, width=GAME_BASE, height=GAME_HEIGHT, border_width=3, corner_radius=2,background_color=BLACK,border_color=BLACK,alpha=100)
    window.pack(background, (0,0))

    background = mu.Background(window, width=500, height=400, border_width=6, corner_radius=10,background_color=VERY_DARK_PICKLE_GREEN,border_color=OFF_GREY,alpha=255)
    window.pack(background, (100,150))

    grid = mu.Grid(columns=10, rows=10, columnwidth=50,rowheight=50)

    # title
    window.set_font_file(os.path.join(f'{os.getcwd()}','assets','titleFont.ttf')) # switch to title font for the title
    label = mu.Label(window, "VERY COOL TANKS", width=1000, text_size=60, text_color=LIGHT_ORANGE,background_alpha=0)
    grid.pack(label, row=0, column=1, columnspan=8, ID="Title")
    window.set_font_file(os.path.join(f'{os.getcwd()}','assets','gameFont.ttf'))
    
    label = mu.Label(window, "Shop", width=300, text_size=40, border_width=0, text_color=LIGHT_ORANGE, background_alpha=0)
    grid.pack(label, row=2, column=4, columnspan=8, ID="WelcomeLabel")
    # end title

    # gold text
    label = mu.Label(window, 
                    "0", 
                    text_center='right',
                    width=85,
                    text_size=16,
                    text_color=LIGHT_ORANGE,
                    border_width=0,
                    background_color=VERY_DARK_PICKLE_GREEN
    )
    window.pack(label, (105,155), ID="GoldNum")

    image = mu.Image(window, image_path=os.path.join(os.getcwd(),'assets','images','Gold.png'),width=20,height=20)
    window.pack(image, (110, 162), ID="GoldImage")
    # end gold text
    window.create_link("GoldNum", linked_id="GoldImage", backward=False)

    # put buttons
    start_coord = ((133,255),(135,404),(140, 413), (135,357),(112,205))
    x_gap = 166
    coords = [[(x+x_gap*i,y) for x,y in start_coord] for i in range(3)]
    fl = [
        ['Distance', os.path.join(os.getcwd(),'assets','images','BulletRange.png'), coords[0], 300],
        ['Speed', os.path.join(os.getcwd(),'assets','images','Speed.png'), coords[1], 400],
        ['Health', os.path.join(os.getcwd(),'assets','images','Health.png'), coords[2], 3000],
    ]
    for cost_ID, image_link, coords, price in fl:
        image = mu.Image(window, image_path=image_link, width=100, height=140)
        window.pack(image, coords[0], ID=cost_ID+"Image")

        button = mu.Button(window, 
                        command=menu.upgrade, # change this later
                        args= (cost_ID,),
                        text = str(price), 
                        text_center='right',
                        width=80,
                        text_size=16,
                        text_color=VERY_DARK_PICKLE_GREEN,
                        border_width=3,
                        background_color=LIGHT_ORANGE
        )
        window.pack(button, coords[1], ID=cost_ID+"Cost")
        image = mu.Image(window, image_path=os.path.join(os.getcwd(),'assets','images','Gold.png'),width=20,height=20)
        window.pack(image, coords[2], ID=cost_ID+"GoldImage")
        
        window.create_link(cost_ID+"Cost", linked_id=cost_ID+"GoldImage", backward=False)

        label = mu.Label(window, 
                        text = "1", 
                        text_center='right',
                        width=80,
                        text_size=16,
                        text_color=LIGHT_ORANGE,
                        border_width=0,
                        background_color=VERY_DARK_PICKLE_GREEN
        )
        window.pack(label, coords[3], ID=cost_ID+"LevelNum")
        label = mu.Label(window, 
                        text = "Level:", 
                        text_center='left',
                        width=80,
                        text_size=16,
                        text_color=LIGHT_ORANGE,
                        border_width=0,
                        background_alpha=0
        )
        
        window.pack(label, coords[3], ID=cost_ID+"LevelText")
        window.create_link(cost_ID+"LevelNum", linked_id=cost_ID+"LevelText", backward=False)
        label = mu.Label(window, 
                    cost_ID,
                    text_center="centre",
                    width=124,
                    text_size=30,
                    text_color=LIGHT_ORANGE,
                    background_alpha=0
        )
        window.pack(label,coords[4], ID=cost_ID + 'label')
    # end buttons    
        

    button = mu.Button(window, "Main menu", command=menu.switch_frame, args=("main",), width=-1, text_size=25, border_width=3, corner_radius=2, border_color=OFF_GREY, background_color=LIGHT_ORANGE, text_color=VERY_DARK_PICKLE_GREEN)
    window.pack(button, (289,485), ID="ContinueButton")

    window.pack(grid, (100,50))
    window.save_frame("shop", flush=True)
