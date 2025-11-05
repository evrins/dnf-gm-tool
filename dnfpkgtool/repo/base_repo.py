from abc import ABC, abstractmethod


class BaseRepo(ABC):
    @abstractmethod
    def is_available(self) -> bool:
        pass
