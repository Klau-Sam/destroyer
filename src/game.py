import pygame
import settings

from pygame.locals import *
from player import Player
from myplatform import MyPlatform


class Game:
    def __init__(self):
        pygame.init()
        self.FramePerSec = pygame.time.Clock()

        self.displaysurface = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Game")

        self.PT1 = MyPlatform()
        self.P1 = Player(scale=(settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT))

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.PT1)
        self.all_sprites.add(self.P1)

        self.clock = pygame.time.Clock()


    def new(self):
        """Start a new game"""
        self.run()

    def run(self):
        """Game loop"""
        while True:
            dt = self.clock.tick(settings.FPS) / 1000.0  # seconds since last frame


            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.displaysurface.fill((0,0,0))
            self.P1.move(dt)
            self.all_sprites.draw(self.displaysurface)


            pygame.display.update()
            self.FramePerSec.tick(settings.FPS)


    # def events(self):
    #     """Handle events"""
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             self.running = False

    def update(self):
        """Update game state"""
        pass  # Game logic here

    # def draw(self):
    #     """Render everything"""
    #     self.screen.fill(settings.BLACK)
    #     pygame.display.flip()