import pygame
import settings

from abstract_character import AbstractCharacter


class Enemy(AbstractCharacter):
      def __init__(self, pos=(100, 100)):
        super().__init__(pos=pos)
        self.image = pygame.image.load("enemy.webp")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,settings.WIDTH-40), 0)