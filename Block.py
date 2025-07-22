import pygame as pg

class Block:
    def __init__(self, x, y, w, h):
        self.rect = pg.Rect(x, y, w, h)
    
    def draw(self, screen):
        pg.draw.rect(screen, (180, 200, 255), self.rect)

    def __str__(self):
        return f"Block({self.rect.x}, {self.rect.y}, {self.rect.w}, {self.rect.h})"