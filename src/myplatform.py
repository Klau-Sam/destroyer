import pygame
import settings

class MyPlatform(pygame.sprite.Sprite):
    def __init__(self, pos=(0,0), size=(200, 20), color=(100, 100, 100)):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)