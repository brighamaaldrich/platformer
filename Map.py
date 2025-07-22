import pygame as pg
from Block import Block

class Map:
    def __init__(self, blocks, spawn, finish):
        self.blocks = blocks
        self.blocks.append(Block(-100, -100, 1400, 100))
        self.blocks.append(Block(-100, -100, 100, 1000))
        self.blocks.append(Block(1200, -100, 100, 1000))
        self.spawn = spawn
        self.finish = finish
    
    def draw(self, screen):
        for block in self.blocks:
            block.draw(screen)
        pg.draw.rect(screen, (255, 0, 0), self.spawn)
        pg.draw.rect(screen, (0, 255, 0), self.finish)
