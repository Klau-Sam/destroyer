from typing import Iterable, List

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
            for obj in self.targets:
                if c is obj:
                    continue
                if c.rect.colliderect(obj.rect):
                    c.onCollided(obj)