import pygame
import settings

class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("enemy.webp")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,settings.WIDTH-40), 0)