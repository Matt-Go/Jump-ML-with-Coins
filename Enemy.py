import os
import pygame as pg
import random as rand

from Rectangle import Rectangle
import Var

red_img = pg.image.load(os.path.join('Assets', 'red_rect.png'))

class Enemy(Rectangle):
    """ Creates an enemy """
    def __init__(self, x, y, width, height, WIN):
        super().__init__(x, y, width, height, WIN)
        self.img = pg.transform.scale(red_img, (self.width, self.height))
        self.speed = 5

    def move_enemies(self, enemies):
        """ Moves the enemy to the left at increasing speeds """
        for enemy in enemies:
            enemy.x -= self.speed
            enemy.rect.center = enemy.x + 45, enemy.y + 37
        return enemies

    def out_enemy(self, enemies, ge):
        """ 
        Removes the enemy and increases player fitness if the enemy has left the screen
        """
        for enemy in enemies:
            if enemy.x + enemy.width < 0:
                self.speed += 0.25
                enemies.remove(enemy)
                self.x, self.y = Var.SCREEN_WIDTH, 400
                for g in ge:
                    g.fitness += 0.01
        return ge
