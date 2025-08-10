import pygame

from pygame.locals import *
from settings import PLAYER_HEIGHT, PLAYER_WIDTH, FRIC

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((50, 30))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect()

        self.vec = pygame.math.Vector2  # 2 for two dimensional
        self.pos = self.vec((0, 0))
        self.vel = self.vec(0,0)
        self.acc = self.vec(0,0)

    def move(self):
        self.acc = self.vec(0,0)

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
            print("left")
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
            print("right")

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self._update_width()

    def _update_width(self):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.rect.width = self.pos.x + PLAYER_HEIGHT
        self.rect.height = self.pos.y + PLAYER_WIDTH