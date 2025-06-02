from lib.pymenu import pymenu as mu
from utils.display.colours import *
def create_frames(window:mu.Window, DISPLAY_BASE,DISPLAY_HEIGHT):
    """Creates all frames used in the game"""
    
    # Welcome Frame

    window.save_frame('welcome',flush=True)