import pandas as pd
from common.etls_common import DataPipeline, Extractor, Transformer, Loader
from extractors.generators.date_dimensions_generator import DateDimensionsGenerator
from transformers.generators.date_dimensions_transformer import DateDimensionsTransformer
from app.utilities.decorators import timer
from loguru import logger

class DateDimensionsETL(Extractor, Transformer, Loader, DataPipeline):
    """Indeed ETL class"""
    def __init__(self, start_date: str, end_date: str, staging_csv_file_path: str, production_csv_file_path: str):
        self.start_date, self.end_date = start_date, end_date
        self.file_name = "date_dimensions.csv"
        self.staging_csv_file_path = staging_csv_file_path % {"file_name": self.file_name}
        self.production_csv_file_path = production_csv_file_path % {"file_name": self.file_name}

    def extract(self) -> pd.DataFrame:
        """Extract data from the Indeed Website"""
        date_dimensions_generator = DateDimensionsGenerator()
        date_dimensions_df: pd.DataFrame = date_dimensions_generator.extract(self.start_date, self.end_date)
        date_dimensions_df.to_csv(self.staging_csv_file_path, index=False)
        return date_dimensions_df

    def transform(self, date_dimensions_df: pd.DataFrame) -> pd.DataFrame:
        """Transform data"""
        date_dimensions_df: pd.DataFrame = DateDimensionsTransformer.transform_df(date_dimensions_df)
        return date_dimensions_df

    def load(self, date_dimensions_df: pd.DataFrame) -> bool:
        """Load data into the CSV"""
        date_dimensions_df.to_csv(self.production_csv_file_path, index=False)
        return True
    
    @timer
    def run(self):
        """Run the ETL"""
        dates_dim_df: pd.DataFrame = self.extract()
        dates_dim_transformed_df: pd.DataFrame = self.transform(dates_dim_df)
        is_loaded: bool = self.load(dates_dim_transformed_df)
        return is_loaded
