import pygame
import random

from settings import *

class CustomPlatform(pygame.sprite.Sprite):
    def __init__(self, width=None, height=None, x=None, y=None):
        super().__init__()
        self.width = width if width is not None else random.randint(PLAT_MIN_WIDTH, PLAT_MAX_WIDTH)
        self.height = height if height is not None else 20

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(PLAT_COLOR)

        self.rect = self.image.get_rect(center=(
            x if x is not None else random.randint(0, WIDTH - self.width),
            y if y is not None else random.randint(0, HEIGHT - 30)
        ))


    def updateObject(self, dt):
        """No updates needed for now, but required for compatibility."""
        pass
