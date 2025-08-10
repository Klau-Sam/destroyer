from typing import List

import pygame
from pygame import rect

from pygame.locals import *
from pygame.math import Vector2 as vec

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
        super().__init__(pos=pos)

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

    @property
    def type(self) -> ObjectType:
        return ObjectType.bullet

    def onCollided(self, others: List[GameObject]) -> None:
        print("onCollided")
        print(others)
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

        self.pos.y = self.pos.y = closest.rect.top - self.rect.height
        self.on_ground = True

    def updateObject(self, dt: float):
        super().updateObject(dt)

        # for testing purposes
        print(self.vel)
        print(self.acc)
        print(self.pos)

        # animate
        self._animate(dt)
        self.acc.x = 0

    def move(self, dt: float):
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