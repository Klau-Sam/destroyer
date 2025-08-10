import pygame

from pygame.locals import *
from settings import FRIC, ACC
from pygame.math import Vector2 as vec


class Player(pygame.sprite.Sprite):
    def __init__(self,
                 pos=(0, 0),
                 idle_path="assets/player_idle.webp",
                 walk_pattern="assets/player_walk_{i}.webp",  # expects i = 0..walk_frames-1
                 walk_frames=4,
                 scale=None,
                 anim_fps=10):
        super().__init__()

        # ---------- load images ----------
        idle_img = pygame.image.load(idle_path).convert_alpha()
        walk_imgs = [
            pygame.image.load(walk_pattern.format(i=i)).convert_alpha()
            for i in range(walk_frames)
        ]

        if scale:
            idle_img = pygame.transform.smoothscale(idle_img, scale)
            walk_imgs = [pygame.transform.smoothscale(img, scale) for img in walk_imgs]

        self.idle_right = idle_img
        self.walk_right = walk_imgs

        # Sprite-required fields
        self.image = self.idle_right
        self.rect = self.image.get_rect(topleft=pos)

        # Physics-ish state
        self.pos = vec(pos)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        # Animation state
        self.facing_right = True
        self.walking = False
        self.frame_index = 0
        self.anim_timer = 0.0
        self.anim_frame_time = 1.0 / float(anim_fps)

    def move(self, dt: float):
        self.acc.update(0, 0)

        pressed = pygame.key.get_pressed()

        if pressed[K_LEFT]:
            self.acc.x = -ACC
            self.facing_right = False
        if pressed[K_RIGHT]:
            self.acc.x = ACC
            self.facing_right = True

        # Simple “friction”
        self.acc.x += self.vel.x * FRIC

        # Integrate
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # walking only when actually moving (tweak threshold if needed)
        self.walking = abs(self.vel.x) > 0.05

        # animate & sync rect
        self._animate(dt)
        self._update_rect()

    def _animate(self, dt: float):
        if self.walking and self.walk_right:
            self.anim_timer += dt
            if self.anim_timer >= self.anim_frame_time:
                self.anim_timer -= self.anim_frame_time
                self.frame_index = (self.frame_index + 1) % len(self.walk_right)

            frame = self.walk_right[self.frame_index]
            if self.facing_right:
                self.image = frame
            else:
                self.image = pygame.transform.flip(frame, True, False)
        else:
            # idle
            self.image = self.idle_right if self.facing_right else pygame.transform.flip(self.idle_right, True, False)

    def _update_rect(self):
        # Set rect to the top-left of your current position
        self.rect.topleft = (self.pos.x, self.pos.y)