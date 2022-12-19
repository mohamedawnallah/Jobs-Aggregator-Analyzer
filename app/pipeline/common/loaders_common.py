class CSVPersistenceManager(ABC):
    """Persistence Manager Abstract Class for other Web Scrappers"""

    @staticmethod
    @abstractmethod
    def write_to_csv(
        csv_file_name: str,
        jobs: Any,
        *args,
        **kwargs
    ) -> int:
        """Save jobs depending on the website also the passed job title"""
        pass

class DBPersistenceManager(ABC):
    """Persistence Manager Abstract Class for other Web Scrappers"""

    @staticmethod
    @abstractmethod
    def write_to_db(
        db_file_name: str,
        jobs: Any
    ) -> int:
        """Save jobs depending on the website also the passed job title"""