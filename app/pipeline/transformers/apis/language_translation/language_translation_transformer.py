from typing import List, Optional
import pandas as pd
from pipeline.common.transformers_common import DataFrameTransformer
from loguru import logger
from pipeline.utilities.utils import Utils
import json
import asyncio
import time
class LanguageTranslationTransformer(DataFrameTransformer):
    
    @staticmethod
    async def transform_df(df: pd.DataFrame, columns_to_translate: List[str],  source_language: Optional[str]='auto', target_language: Optional[str] = 'en') -> pd.DataFrame:
        for index, row in df.iterrows():
            for column in columns_to_translate:
                text = str(row[column])
                translated_text = await LanguageTranslationTransformer.translate(text, source_language, target_language)
                df.at[index, column] = translated_text
                time.sleep(1)
        return df
   
    @staticmethod
    async def translate(text: str, source_language: Optional[str]='auto', target_language: str = 'en') -> str:
        if not text or text == 'nan':
            return text
        response = await Utils.request_url("http://localhost:5000/translate", http_method="POST", data={'q':text,'source':source_language,'target':target_language,'format':'text'}, content_type='application/json')
        translated_text = json.loads(response)["translatedText"]
        return translated_text
    
    

