import os
import pygame as pg

from Rectangle import Rectangle
import Var

yellow_img = pg.image.load(os.path.join('Assets', 'yellow_circle.png'))

class Coin(Rectangle):
    def __init__(self, x, y, width, height, WIN):
        """ Creates a coin """
        super().__init__(x, y, width, height, WIN)
        self.img = pg.transform.scale(yellow_img, (self.width, self.height))
        self.delete = False
