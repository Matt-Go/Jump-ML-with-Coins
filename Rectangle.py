import pygame as pg

class Rectangle(object):
    """ Creates a rectangle """
    def __init__(self, x, y, width, height, WIN):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.WIN = WIN

    def draw(self):
        """ Draws the rectangle """
        self.WIN.blit(self.img, (self.x, self.y))

    def draw_mult(self, shapes):
        """ Draws multiple rectangles """
        for shape in shapes:
            shape.draw()

    def check_collision(self, player, rect):
        """ Checks if player collides with enemy or coin"""
        player_mask = player.get_mask()
        rect_mask = pg.mask.from_surface(rect.img)
        offset = (round(rect.x) - round(player.x), round(rect.y) - round(player.y))
        point = player_mask.overlap(rect_mask, offset)
        if point:
            return True
        return False
    