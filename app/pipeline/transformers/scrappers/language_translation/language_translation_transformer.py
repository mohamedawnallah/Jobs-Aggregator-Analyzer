from typing import List, Optional
import pandas as pd
from pipeline.common.transformers_common import DataFrameTransformer
from loguru import logger
from deep_translator import GoogleTranslator
from pipeline.utilities.utils import Utils
import json
import asyncio

class LanguageTranslationTransformer(DataFrameTransformer):
    @staticmethod
    async def transform_df(df: pd.DataFrame, columns_to_translate: List[str],  source_language: Optional[str]='auto', target_language: Optional[str] = 'en') -> pd.DataFrame:
        # Translate the columns asynchronoulsy
        translation_tasks = []
        for _, row in df.iterrows():
            for column in columns_to_translate:
                translation_tasks.append(asyncio.create_task(LanguageTranslationTransformer.translate(row[column], source_language, target_language)))
                await asyncio.sleep(0.5)
        df = await asyncio.gather(*translation_tasks)
        return df
   
    @staticmethod
    async def translate(text: str, source_language: Optional[str]='auto', target_language: str = 'en') -> str:
        response = await Utils.request_url("http://localhost:5000/translate", http_method="POST", data={'q':text,'source':source_language,'target':target_language,'format':'text'}, content_type='application/json')
        translated_text = json.loads(response)["translatedText"]
        logger.info(f"Translated {text} to {translated_text}")
        return translated_text
    
    

