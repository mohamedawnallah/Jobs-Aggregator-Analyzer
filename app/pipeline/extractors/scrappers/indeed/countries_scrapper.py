from typing import Optional, AsyncGenerator, Generator
import pandas as pd
import bs4
from bs4 import BeautifulSoup
from pipeline.common.scrappers_common import CountriesScrapper
from models.country_model import CountryDim
from pipeline.utilities.utils import Utils
from pipeline.common.etls_common import ExtractorAsync
from models.country_model import CountryDim
from transformers.scrappers.indeed.countries_transformer import IndeedCountriesTransformer

class IndeedCountriesScrapper(CountriesScrapper, ExtractorAsync):
    
    async def extract(self, countries_url: str, countries_no: int) -> pd.DataFrame:
        countries_generator: AsyncGenerator[CountryDim,None] = self.get_countries(countries_url=countries_url, countries_no=countries_no)
        countries_df: pd.DataFrame =  await self.get_countries_df(countries_generator)
        return countries_df
        
    async def get_countries(self, countries_no: Optional[int] = None, countries_url: str = None) -> AsyncGenerator[CountryDim, None]:
        """Get the list of countries supported by indeed"""
        countries_soup: BeautifulSoup =  await Utils.get_page_parsed(countries_url)
        worldwide_countries: Optional[bs4.element.ResultSet] = Utils.find_bs4_elements(countries_soup, "li", {"class":"worldwide__country"})
        countries_number = len(worldwide_countries) if not countries_no else countries_no
        for pos in range(countries_number):
            country: bs4.element.Tag = worldwide_countries[pos]
            country: CountryDim = IndeedCountriesTransformer.transform(country)
            yield country
            
    async def get_countries_df(self, countries_generator: AsyncGenerator[CountryDim,None]) -> pd.DataFrame:
        countries_df: Optional[pd.DataFrame] = None
        indx = 1
        async for country in countries_generator:
            if indx == 1:
                countries_df = pd.DataFrame(country.to_dict(), index=[indx])
            else:
                new_countries_df = pd.DataFrame(country.to_dict(), index=[indx])
                countries_df = pd.concat([countries_df, new_countries_df],axis=0)
            indx += 1
        return countries_df
    
    @staticmethod   
    def get_countries_from_local(production_countries_path: str) -> Generator[CountryDim, None, None]:
        countries_df: pd.DataFrame = pd.read_csv(production_countries_path)
        for _, country in countries_df.iterrows():
            country_dim = CountryDim(country_id=country['country_id'],country_name=country['country_name'],
                                     country_code=country['country_code'],country_url=country['country_url'])
            yield country_dim           
    
    