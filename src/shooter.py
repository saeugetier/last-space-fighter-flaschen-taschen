#
# Space shooter
#
# Author : yuiio@sotodesign.org

from os.path import join as path_join
from time import time

import pyxel as px

from constants import *
from game import Game

import flaschen

import ctypes

import numpy as np


# Define the palette
palette = [
    (0, 0, 0),       # BLACK
    (0, 0, 255),     # BLUE
    (128, 0, 128),   # PURPLE
    (0, 128, 0),     # DARK_GREEN
    (139, 69, 19),   # BROWN
    (128, 128, 128), # GREY
    (192, 192, 192), # LIGHT_GREY
    (255, 255, 255), # WHITE
    (255, 0, 0),     # RED
    (255, 165, 0),   # ORANGE
    (255, 255, 0),   # YELLOW
    (0, 255, 0),     # GREEN
    (0, 255, 255),   # CYAN
    (255, 0, 255),   # LIGHT_PURPLE
    (255, 192, 203), # PINK
    (255, 228, 196)  # FLESH
]

class App:
    ft = None
    def __init__(self):
        px.init(WIDTH, HEIGHT, title="The last space fighter", capture_sec=0)
        self.ft = flaschen.Flaschen("localhost", 1337, WIDTH, HEIGHT)
        px.load(path_join("assets", "shooter.pyxres"))
        #px.fullscreen(True)

        self.pt = time()  # Buffer previous time
        self.game = Game()
        self.paused = False

        px.mouse(SHOW_CURSOR)
        px.run(self.update, self.draw)

    def update(self):

        if px.btnp(px.KEY_Q):
            px.quit()
        if px.btnp(px.KEY_P):
            if not self.paused:
                px.stop()
            else:
                self.pt = time()
                px.playm(3, loop=True)
            self.paused = not self.paused

        if not self.paused:
            t = time()
            dt = t - self.pt
            self.pt = t

            self.game.state.update(dt, t)
            self.game.state = self.game.state.get_next_state()

    def draw(self):
        if not self.paused:
            self.game.state.draw()
          
        pixeldata = px.screen.data_ptr()  
        #print(pixeldata)
        # Map each pixel value to its corresponding RGB value
        rgb_array = np.array([palette[pixel] for pixel in pixeldata], dtype=np.uint8)
        # Reshape the array to (128, 192, 3)
        reshaped_array = rgb_array.reshape((128, 192, 3))
        # Convert the reshaped array to a tuple of tuples if needed
        reshaped_tuple = tuple(map(tuple, reshaped_array))

        self.ft.send_array(reshaped_array, (0,0,0))


App()
