import string
from abc import ABC, abstractmethod
from typing import List

import pygame
from pygame.math import Vector2 as vec

import settings
from collidable import Collidable
from gameobject import GameObject
from objecttype import ObjectType


class AbstractCharacter(GameObject, Collidable, ABC):
    def __init__(self, idle_path: string, walk_pattern: string,
                 walk_frames: int, anim_fps=10, scale=None, pos=(0, 0), gravity=0.5, friction=-1, ):
        super().__init__()
        # Position and movement variables
        self.pos = vec(pos)
        self.vel = vec(0, 0)
        self.acc = vec(0, gravity)  # Gravity by default

        # Physics-related constants
        self.gravity = gravity
        self.friction = friction
        self.on_ground = False
        self.facing_right = True


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

        # Animation state
        self.walking = False
        self.frame_index = 0
        self.anim_timer = 0.0
        self.anim_frame_time = 1.0 / float(anim_fps)

    @abstractmethod
    def updateObject(self, dt: float):
        """
        Update the character's state (position, velocity, etc.).
        Subclasses must implement specific details (e.g., enemy AI or player input handling).
        """
        # Gravity
        self.acc.y = 0.0 if self.on_ground else 0.5
        # Simple "friction"
        self.acc.x += self.vel.x * self.friction
        # Integrate motion (acceleration -> velocity -> position)
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # Reset horizontal acceleration
        self._animate(dt)
        self.acc.x = 0

        # Sync rect position with the current character position
        self._update_rect()

    def onCollided(self, others: List[GameObject]) -> None:
        self._checkIfObjectIsOnTheGround(others)

    def _checkIfObjectIsOnTheGround(self, others: List[GameObject]):
        self.on_ground = False

        floors = [e for e in others if e.type == ObjectType.floor]
        if not floors:
            return

        floors_to_land = list(filter(lambda f: 0 <= self.rect.bottom - f.rect.top <= 50, floors))

        if not floors_to_land:
            return

        print(floors_to_land)
        closest = floors_to_land[0]

        self.pos.y = closest.rect.top - self.rect.height + 1
        self.on_ground = True

    def moveLeft(self):
        """Move the character to the left by applying negative acceleration."""
        self.acc.x = -settings.ACC
        self.facing_right = False

    def moveRight(self):
        """Move the character to the right by applying positive acceleration."""
        self.acc.x = settings.ACC
        self.facing_right = True

    def _update_rect(self):
        """Update the sprite's rect position based on the current position vector."""
        if self.rect:
            self.rect.topleft = (self.pos.x, self.pos.y)


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