import pygame
from abc import ABC, abstractmethod

from objecttype import ObjectType


class GameObject(pygame.sprite.Sprite, ABC):
    def __init__(self, rect: pygame.Rect | None = None):
        super().__init__()
        # Subclasses can overwrite this after setting their image.
        self.rect: pygame.Rect = rect or pygame.Rect(0, 0, 0, 0)

    def isCollided(self, other: "GameObject") -> bool:
        return self.rect.colliderect(other.rect)

    @abstractmethod
    def updateObject(self, dt: float) -> None:
        pass

    @property
    @abstractmethod
    def type(self) -> ObjectType:
        pass