import pygame as pg
import sys, json, os

WIDTH = 1200
HEIGHT = 800

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Platformer")

with open("map.json", "r") as f:
    data = json.load(f)
    blocks = data.get("blocks", [])
    spawn = data.get("spawn", None)
    finish = data.get("finish", None)

start    = None
dragging = False
ctrl     = False

def round50(n, base=50):
    return base * round(n/base)

def snapPos(pos):
    x, y = pos
    if x % 50 < 8 or x % 50 > 41:
        x = round50(x)
    if y % 50 < 8 or y % 50 > 41:
        y = round50(y)
    return (x, y)

def drawGrid():
    for c in range(24):
        for r in range(16):
            x, y = c * 50, r * 50
            pg.draw.rect(screen, (30, 30, 30), (x, y, 50, 50), 1)
    for c in range(6):
        for r in range(4):
            x, y = c * 200, r * 200
            pg.draw.rect(screen, (100, 100, 100), (x, y, 200, 200), 1)

def getFileName():
    files = os.listdir("levels")
    if len(files) == 1: return "level1.json"
    files.sort(key=lambda x: int(x[5:-5]))
    return f"levels/level{int(files[-1][5:-5]) + 1}.json"

def doQuit(blocks, spawn, finish):
    pg.quit()
    print(getFileName())
    with open(getFileName(), 'w') as f:
        json.dump({
            "blocks": blocks,
            "spawn": spawn,
            "finish": finish
        }, f)
    with open(f"map.json", "w") as f:
        json.dump({
            "blocks": blocks,
            "spawn": spawn,
            "finish": finish
        }, f)
    sys.exit()

def getRect(start):
    end = snapPos(pg.mouse.get_pos())
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(end[0] - start[0])
    h = abs(end[1] - start[1])
    return (x, y, w, h)

def drawLevel(blocks, spawn, finish, dragging, start):
    drawGrid()
    for block in blocks:
        pg.draw.rect(screen, (30, 70, 220), block)
        pg.draw.rect(screen, (0, 0, 80), block, 4)
    if spawn: pg.draw.rect(screen, (0, 200, 0), spawn)
    if finish: pg.draw.rect(screen, (255, 0, 0), finish)
    if dragging:
        block = getRect(start)
        pg.draw.rect(screen, (65, 105, 255), block)

def deleted(rect):
    return pg.Rect(rect).collidepoint(pg.mouse.get_pos())

while True:
    screen.fill((0, 0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            doQuit(blocks, spawn, finish)
        elif event.type == pg.KEYDOWN and event.key == pg.K_LCTRL:
            ctrl = True
        elif event.type == pg.KEYUP and event.key == pg.K_LCTRL:
            ctrl = False
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            dragging = True
            start = snapPos(pg.mouse.get_pos())
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            if spawn and deleted(spawn): spawn = None
            if finish and deleted(finish): finish = None
            kf = lambda b: not deleted(b)
            blocks = list(filter(kf, blocks))
        elif event.type == pg.MOUSEBUTTONUP and dragging:
            dragging = False
            x, y, w, h = getRect(start)
            if ctrl and spawn:
                if w >= 5 and h >= 5: finish = (x, y, w, h)
            elif ctrl:
                if w >= 5 and h >= 5: spawn = (x, y, w, h)
            else:
                if w >= 5 and h >= 5: blocks.append((x, y, w, h))
    drawLevel(blocks, spawn, finish, dragging, start)
    pg.display.update()
