from abc import ABC, abstractmethod

import pygame
from pygame.math import Vector2 as vec

import settings
from collidable import Collidable
from gameobject import GameObject


class AbstractCharacter(GameObject, Collidable, ABC):
    def __init__(self, pos=(0, 0), gravity=0.5, friction=-1):
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

        # Rect (to be implemented by subclasses)
        self.image = None
        self.rect = None

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
        self.acc.x = 0

        # Sync rect position with the current character position
        self._update_rect()

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