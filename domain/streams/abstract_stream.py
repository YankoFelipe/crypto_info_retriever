from abc import ABC, abstractmethod


class AbstractStream(ABC):
    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def is_alive(self) -> bool:
        pass
