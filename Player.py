import pygame as pg
from enum import Enum

class CollisionType(Enum):
    LEFT   = (-1, 0)
    RIGHT  = (1, 0)
    TOP    = (0, -1)
    BOTTOM = (0, 1)
    NONE   = (0, 0)

class Player:
    def __init__(self, w, h, maps):
        self.rect        = pg.Rect(0, 0, w, h)
        self.rect.center = maps[0].spawn.center
        self.y_vel       = 0
        self.x_vel       = 0
        self.gravity     = -0.12

        self.left        = False
        self.right       = False

        self.lives       = 5
        self.dmg_cd      = 0
        self.jumps       = 0

        self.ghost       = [pg.Rect.copy(self.rect) for _ in range(12)]
        self.frame       = 0

        self.maps        = maps
        self.map_index   = 0

    def draw(self, screen):
        map = self.maps[self.map_index]
        map.draw(screen)
        n = len(self.ghost)
        for i, g in enumerate(self.ghost):
            scale_factor = 15 / ((n-i) + 17)
            x, y, w, h = g.scale_by(scale_factor)
            s = pg.Surface((w, h))
            s.set_alpha(int((scale_factor**4) * 255))
            s.fill((255,255,255))
            screen.blit(s, (x, y))
        pg.draw.rect(screen, (255, 255, 255), self.rect)
    
    def update(self, WIDTH, HEIGHT):
        map = self.maps[self.map_index]
        self.frame += 1
        if self.frame % 3 == 0:
            self.ghost.append(self.rect.copy())
            self.ghost.pop(0)

        self.rect.move_ip(self.x_vel, -self.y_vel)
        self.x_vel += 0.08 if self.right else 0
        self.x_vel -= 0.08 if self.left else 0
        self.x_vel *= 0.97
        self.y_vel += self.gravity

        if self.rect.bottom > HEIGHT:
            self.rect.center = map.spawn.center
            self.y_vel = 0
            self.x_vel = 0

        self.collideMap()

    
    def jump(self):
        if self.jumps > 0:
            self.y_vel = 6
            self.jumps -= 1

    def collideMap(self):
        map = self.maps[self.map_index]
        for block in map.blocks:
            self.collideBlock(block)
        if self.rect.colliderect(map.finish):
            self.map_index += 1
            self.map_index %= len(self.maps)
            map = self.maps[self.map_index]
            self.rect.center = map.spawn.center
            self.y_vel = 0
            self.x_vel = 0
    
    def collideBlock(self, block):
        c = self.getCollisionType(block)
        if c == CollisionType.RIGHT:
            self.rect.left = block.rect.right
            self.x_vel = 0
        elif c == CollisionType.LEFT:
            self.rect.right = block.rect.left
            self.x_vel = 0
        elif c == CollisionType.TOP:
            self.rect.bottom = block.rect.top
            self.y_vel = 0
            self.jumps = 2
        elif c == CollisionType.BOTTOM:
            self.rect.top = block.rect.bottom
            self.y_vel = 0

    def getCollisionType(self, block):
        if not self.rect.colliderect(block.rect):
            return CollisionType.NONE
        x, y, w, h = self.rect
        bx, by, bw, bh = block.rect
        x_overlap = min(bx - x - w, bx + bw - x, key=abs)
        y_overlap = min(by - y - h, by + bh - y, key=abs)
        if abs(y_overlap) < abs(x_overlap):
            if y_overlap < 0 and self.y_vel < 0:
                return CollisionType.TOP
            elif y_overlap > 0 and self.y_vel > 0:
                return CollisionType.BOTTOM
        elif abs(y_overlap) > abs(x_overlap):
            if x_overlap < 0 and self.x_vel > 0:
                return CollisionType.LEFT
            elif x_overlap > 0 and self.x_vel < 0:
                return CollisionType.RIGHT
        return CollisionType.NONE