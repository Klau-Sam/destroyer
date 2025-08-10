from abc import abstractmethod, ABC

from gameobject import GameObject

class Collidable(ABC):  # type: ignore[name-defined]
    @abstractmethod
    def onCollided(self, other: GameObject) -> None:
        pass
