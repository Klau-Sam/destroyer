from typing import List

import pygame

from pygame.locals import *

from abstract_character import AbstractCharacter
from gameobject import GameObject
from objecttype import ObjectType


class Player(AbstractCharacter):
    def __init__(self,
                 pos=(0, 0),
                 idle_path="assets/player_idle.webp",
                 walk_pattern="assets/player_walk_{i}.webp",  # expects i = 0..walk_frames-1
                 walk_frames=4,
                 scale=None,
                 anim_fps=10):
        super().__init__(idle_path=idle_path, walk_pattern=walk_pattern, walk_frames=walk_frames, scale=scale,
                         anim_fps=anim_fps, pos=pos)

    @property
    def type(self) -> ObjectType:
        return ObjectType.bullet

    def updateObject(self, dt: float):
        super().updateObject(dt)

    def move(self):
        pressed = pygame.key.get_pressed()
        self.walking = True
        if pressed[K_LEFT]:
            self.moveLeft()
        elif pressed[K_RIGHT]:
            self.moveRight()
        elif pressed[K_UP]:
            self.jump()
        else:
            self.walking = False

    def jump(self):
        if self.on_ground:
            self.vel.y = -15
