from typing import Iterable, List

import pygame

from collidable import Collidable
from gameobject import GameObject


class CollisionHelper:
    """Checks collisions between `collidables` and `targets` and calls onCollided()."""
    def __init__(self,
                 collidables: Iterable[Collidable],
                 targets: Iterable[GameObject]):
        self.collidables: List[Collidable] = list(collidables)
        self.targets: List[GameObject] = list(targets)

    def checkCollisions(self) -> None:
        """Call each frame: triggers onCollided for any overlapping pairs."""
        for c in self.collidables:
            hits = pygame.sprite.spritecollide(c , self.targets, False)
            # collect all unique overlaps; skip self
            c.onCollided(hits)