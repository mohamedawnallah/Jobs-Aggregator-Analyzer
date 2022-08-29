from abc import abstractmethod, ABC
from typing import Any

class Extractor(ABC):
    """Extractor"""
    @abstractmethod
    def extract(self, *args, **kwargs) -> Any:
        """Extract data from Scrappers"""

class Transformer(ABC):
    """Transformer"""
    @abstractmethod
    def transform(self, *args, **kwargs) -> Any:
        """Transform data"""

class Loader(ABC):
    """Loader"""
    @abstractmethod
    def load(self, *args, **kwargs) -> Any:
        """Load data into one of the provided persistence managers"""

class ETL(ABC):
    """ETL"""
    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """Run the ETL"""