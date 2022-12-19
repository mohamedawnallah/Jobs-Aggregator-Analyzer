from abc import ABC, abstractmethod

class Transformer(ABC):
    """Transformer Abstract Class"""
    @abstractmethod
    def transform(*args, **kwargs) -> None:
        """Transform the data"""
        
class DataFrameTransformer(ABC):
    """Transformer Data Frame"""
    
    @abstractmethod
    def transform_df(*args, **kwargs) -> None:
        """Transform the data frame"""

