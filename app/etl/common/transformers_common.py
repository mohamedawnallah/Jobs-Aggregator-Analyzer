from abc import ABC, abstractmethod

class Transformer(ABC):
    """Transformer Abstract Class"""
    @staticmethod
    @abstractmethod
    def transformer(*args, **kwargs) -> None:
        """Transform the data"""

