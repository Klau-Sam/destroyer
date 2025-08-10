from abc import abstractmethod, ABC
from typing import List

from gameobject import GameObject

class Collidable(ABC):  # type: ignore[name-defined]
    @abstractmethod
    def onCollided(self, others: List[GameObject]) -> None:
        pass
