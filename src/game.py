import pygame
import settings

from pygame.locals import *
from player import Player
from custom_platform import CustomPlatform
from collisionhelper import CollisionHelper


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.displaysurface = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Game")

        self.clock = pygame.time.Clock()

    def new(self):
        """Start a new game"""
        self.platforms = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.P1 = Player(scale=(settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT))
        bottom_platform = CustomPlatform(width=settings.WIDTH, height=20, x=settings.WIDTH // 2,
                       y=settings.HEIGHT - 10)
        self.platforms.add(bottom_platform)
        self.all_sprites.add(self.P1)
        self.all_sprites.add(bottom_platform)

        self.generate_platforms()
        self.collisionsHelper = CollisionHelper([self.P1], [bottom_platform])

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
            self.collisionsHelper.checkCollisions()

            for sprite in self.all_sprites:
                sprite.updateObject(dt)

            self.all_sprites.draw(self.displaysurface)

            pygame.display.update()
            self.clock.tick(settings.FPS)

            hits = pygame.sprite.spritecollide(self.P1 , self.platforms, False)
            if self.P1.vel.y > 0: 
                if hits:
                    self.P1.pos.y = hits[0].rect.top + 1 - settings.PLAYER_HEIGHT
                    self.P1.vel.y = 0


    # def events(self):
    #     """Handle events"""
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             self.running = False

    def update(self):
        """Update game state"""
        pass  # Game logic here

    def generate_platforms(self):
        """Generate platforms without overlap."""
        required_platforms = 6  # Number of platforms needed
        while len(self.platforms) < required_platforms:
            new_platform = CustomPlatform()  # Create a new random platform

            # Check for collision with existing platforms
            collision = pygame.sprite.spritecollide(
                new_platform, self.platforms, False, collided=pygame.sprite.collide_rect
            )

            if not collision:  # If no collision, add the platform
                self.platforms.add(new_platform)
                self.all_sprites.add(new_platform)

    # def draw(self):
    #     """Render everything"""
    #     self.screen.fill(settings.BLACK)
    #     pygame.display.flip()