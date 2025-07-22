import pygame as pg
import sys, json, os
from Player import Player
from Map import Map
from Block import Block


WIDTH = 1200
HEIGHT = 800
FPS = 300

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT), flags=0, depth=32)
pg.display.set_caption("Platformer")
clock = pg.time.Clock()

def makeBlock(b):
    return Block(b[0], b[1], b[2], b[3])

def getFile(path):
    with open(f'levels/{path}', 'r') as f:
        return json.load(f)

def getMap(data):
    blocks = [makeBlock(b) for b in data["blocks"]]
    spawn = pg.Rect(data["spawn"])
    finish = pg.Rect(data["finish"])
    return Map(blocks, spawn, finish)

paths = os.listdir("levels")
paths.sort(key=lambda x: int(x[5:-5]))
files = map(getFile, paths)
maps = list(map(getMap, files))


p = Player(30, 30, maps)


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                p.jump()
            if event.key == pg.K_LEFT:
                p.left = True
            if event.key == pg.K_RIGHT:
                p.right = True
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                p.left = False
            if event.key == pg.K_RIGHT:
                p.right = False

    screen.fill((0, 0, 0))

    p.draw(screen)
    p.update(WIDTH, HEIGHT)

    pg.display.update()
    clock.tick(FPS)
    pg.display.set_caption(f"Platformer    |    FPS: {int(clock.get_fps())}")