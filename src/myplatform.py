import pygame

from gameobject import GameObject


class MyPlatform(GameObject):
    def __init__(self, pos=(0, 0), size=(200, 20), color=(100, 100, 100), one_way=False):
        super().__init__()
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)
        self.one_way = one_way

    def updateObject(self, dt: float):

        pass