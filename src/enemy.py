import random
from typing import List

import pygame
import settings

from abstract_character import AbstractCharacter
from gameobject import GameObject
from objecttype import ObjectType


class Enemy(AbstractCharacter):
    def __init__(self,
                 pos=(0, 0),
                 idle_path="assets/enemy.webp",
                 walk_pattern="assets/enemy_walking_1.webp",
                 walk_frames=1,
                 scale=None,
                 anim_fps=10):
        super().__init__(idle_path=idle_path, walk_pattern=walk_pattern, walk_frames=walk_frames, scale=scale,
                         anim_fps=anim_fps, pos=pos)

    def updateObject(self, dt: float):
        super().updateObject(dt)

    @property

    def type(self) -> ObjectType:
        return ObjectType.enemy
