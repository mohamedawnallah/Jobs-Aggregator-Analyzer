from typing import Generator
import os
import json
import sys
import csv
from typing import Optional
import toml
import bs4
from bs4 import BeautifulSoup
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import Utils
import utils.helpers as helpers

from utils.helpers import Scrapper,Company,JobBasicInfo,JobAdditionalInfo
from utils.constants import CONFIGS_PATH

class IndeedScrapper(Scrapper):
    """Scrapper f"""
    """Scrapper for Indeed Jobs"""
    def __init__(self, configs: dict, skills_config_name: str):
        "Initialize the Indeed Scrapper"
        self.countries_base_url = configs['indeed']['countries_base_url']
        self.jobs_base_url = configs['indeed']['jobs_base_url']
        self.job_base_url = configs['indeed']['job_base_url']
        self.company_base_url = configs['indeed']['company_base_url']
        self.job_skills = configs[skills_config_name]

    def get_countries(self, end_pos: Optional[int] = None) -> dict:
        """Get the list of countries supported by indedd"""
        countries_response = requests.get(self.countries_base_url)
        countries_soup = BeautifulSoup(countries_response.text, 'html.parser')
        results = countries_soup.find('ul', class_='worldwide__countries')
        countries_raw = results.find_all('a')
        countries_dict: dict = {}
        end_pos = len(countries_raw) if end_pos is None else end_pos
        for pos in range(0,end_pos):
            country = countries_raw[pos]
            country_name = country.text.strip()
            country_link = country.get('href').strip()
            subdomain = country_link.split('//')[1].split('.')[0]
            country_code = subdomain
            country = {country_name: country_code}
            countries_dict.update(country)
        
        return countries_dict

 
    def get_jobs_countries(self, countries_input: dict, job_title_input: str, page_no: Optional[int] = None) -> Generator[Generator[dict,None,None],None,None]:
        """Get the list of jobs"""
        for country_name, country_code in countries_input.items():
            jobs_url = self.jobs_base_url % {'country_code':country_code,'job_title':job_title_input}
            print("Job Url: ", jobs_url)
            max_page_no =  page_no if page_no else self.get_pages_no(jobs_url)
            yield self.get_jobs_for_each_page(jobs_url,max_page_no,country_name)

    def get_pages_no(self,jobs_url: str) -> int:
        """Get the number of pages"""
        jobs_url_paged = jobs_url + '&start=' + "1000000"

        try:
            results = IndeedScrapper.get_results_job_cards_col(jobs_url_paged)
            search_count_raw = results.find('div', id='searchCountPages')
            numbers = [int(s) for s in search_count_raw.split() if s.isdigit()]
            max_page_no = numbers[0] * 10
        except (AttributeError,TypeError,IndexError) as a_e:
            max_page_no = 200
            return max_page_no
        return max_page_no

        
    def get_jobs_for_each_page(self,jobs_url: str,max_page_no: int, country_name:str):
        """Get jobs for each country supported by indeed jobs website"""
        for page_no in range(0, max_page_no, 10):
            try:
                jobs_url_paged = jobs_url + '&start=' + str(page_no)
                results = IndeedScrapper.get_results_job_cards_col(jobs_url_paged)
                jobs_raw_page = results.find_all('div', class_='cardOutline')
            except AttributeError as a_e:
                #TODO Logging 
                continue 

            jobs_page_gen: Generator[dict,None,None] = self.get_basic_job_info(jobs_raw_page, country_name)
            return jobs_page_gen
            
            
    def get_basic_job_info(self, jobs_raw_page: bs4.element.ResultSet, country_name: str):
        """Get jobs per page (usually 15 jobs per page in indeed)"""
        for job in jobs_raw_page:
            job_title = job.find('div', class_='heading4').find('a').find('span')
            job_id = job.find('div', class_='heading4').find('a').get('href')
            # choose job type based on div and the class is metadata only
            job_salary = job.find('div', class_='salaryOnly')
            company_name = job.find('span', class_='companyName')
            company_location = job.find('div', class_='companyLocation')
            company_rating = job.find('span', class_='ratingNumber')

            
            job_title = Utils.get_valid_value(job_title)
            job_id = Utils.get_valid_value(job_id)[1:]
            job_link = self.job_base_url % {'job_id':job_id}  
            job_salary = Utils.get_valid_value(job_salary)
            company_name = Utils.get_valid_value(company_name)
            company_website = self.company_base_url % {'company_name':company_name}
            company_location = Utils.get_valid_value(company_location)
            company_rating = Utils.get_valid_value(company_rating)
            
            #company_info named tuple
            company = Company(company_name, company_website, company_location, company_rating,country_name)
            

           
            more_job_info: tuple[str,str,dict,dict]=  self.get_more_job_info(job_link)
            
            job_description,posted_date,job_matched_skills,job_additional_info = more_job_info
        
            job_basic_info = JobBasicInfo(job_title=job_title,
                                          job_description=job_description,
                                          job_link=job_link, job_salary=job_salary,
                                          posted_date=posted_date)

            job_basic_info_kwargs = job_basic_info._asdict()
            company_kwargs = company._asdict()

            job_full_info = {**job_basic_info_kwargs, **company_kwargs,
                             **job_matched_skills, **job_additional_info}

            yield job_full_info      


 
    def get_more_job_info(self,job_link: str) -> tuple[str,str,dict,dict]:
        """Get the more job info"""
        #"Get more job info"
        job_info_soup = Utils.get_page_parsed(job_link)
        root_info = job_info_soup.find('div',id='viewJobSSRRoot')
        benefit_section = root_info.find('div',id='benefits')
        posted_date = root_info.find('div',id='hiringInsightsSectionRoot').find('p',class_='jobsearch-HiringInsights-entry--bullet')
        job_description = root_info.find('div',class_='jobsearch-JobComponent-description')

        root_info = Utils.get_valid_value(root_info).lower()
        cs_degree_needed = Utils.check_degree(['bachelor','computer science'],root_info)
        posted_date = Utils.get_valid_value(posted_date)
        job_description = Utils.get_valid_value(job_description).replace('\n','')
        benefits = IndeedScrapper.get_indeed_job_benefits(benefit_section)   
         
        job_matched_skills: dict = Utils.get_matched_skills(self.job_skills,root_info)
        
        job_additional_info = JobAdditionalInfo(cs_degree_needed,benefits)
        job_additionl_info: dict = job_additional_info._asdict()

        return job_description, posted_date, job_matched_skills, job_additionl_info
    
    @staticmethod
    def get_results_job_cards_col(jobs_url) -> bs4.element.Tag:
        """Get the results column which contain basic job cards info"""
        jobs_soup = Utils.get_page_parsed(jobs_url)
        results = jobs_soup.find('table',id='pageContent')
        return results

    @staticmethod
    def get_indeed_job_benefits(benefits_section):
        """Get the benefits"""
        result =  'N/A' if not benefits_section else benefits_section.find_all('div',class_='css-1f2yqp0 e1xnxm2i0')
        all_benefits = ''
        if result != 'N/A':
            all_benefits = IndeedScrapper.get_readable_job_benefits(result)
        return all_benefits

    @staticmethod
    def get_readable_job_benefits(benefits_raw: str) -> str:
        """Getting jobs benefits mentioned in job indeed page
        Some jobs in indeed have benefits section and others not"""
        benefits_str = ''
        for benefit in benefits_raw:
            benefit_value = Utils.get_valid_value(benefit)
            benefits_str += benefit_value + ', '
        return benefits_str 

    @staticmethod
    def write_to_csv(csv_file_name, jobs: Generator[Generator[dict,None,None],None,None], csv_header: list) -> None:
        """Write data to json file"""
        with open(csv_file_name,'w',encoding='utf-8') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=csv_header)
            csv_writer.writeheader()
            for jobs_country in jobs: 
                for job_page in jobs_country:
                    print(json.dumps(job_page,indent=4))
                    csv_writer.writerow(job_page)
    
if __name__ == '__main__':
    # Read the configs
    configs = toml.load(CONFIGS_PATH)
    skills_config_name = 'data_engineering_skills'
    csv_header = Utils.get_csv_header(configs,skills_config_name)

    job_title_input = 'Data Engineer'
    csv_file_path = f"static/data/{job_title_input}_jobs.csv"

    scrapper = IndeedScrapper(configs,skills_config_name)
   
    countries = scrapper.get_countries()
    
    jobs_gen = scrapper.get_jobs_countries(countries,job_title_input)
    
    IndeedScrapper.write_to_csv(csv_file_path,jobs_gen,csv_header)
