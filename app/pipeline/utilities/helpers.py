class DataFileReaderSingleton:
    __data_from_file: str = None

    @staticmethod
    def get_data(file_path: str) -> str:
        """ Static access method. """
        if DataFileReaderSingleton.__data_from_file is None:
            DataFileReaderSingleton(file_path)
        return DataFileReaderSingleton.__data_from_file

    def __init__(self, file_path: str):
        """ Virtually private constructor. """
        with open(file_path, "r",encoding='utf-8') as file_handler:
            data = file_handler.read().strip().splitlines()
        DataFileReaderSingleton.__data_from_file = data


