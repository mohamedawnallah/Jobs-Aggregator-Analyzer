"""Python script to scrape Datastackjobs.com for job postings.

Datastackjobs.com is a simple job board that displays job postings around the world.

This script automates the process of scraping Datastackjobs.com for job postings
and saves the results in a CSV file(temporary).
"""

import csv
import json
import re
import requests
from bs4 import BeautifulSoup
from etl.utils.utils import Utils

utils = Utils()
configs = utils.get_configs()


class DataStackJobsScraper:
    """Scraper for Datastackjobs.com"""

    def __init__(self, configs: dict):
        self.url: str = configs['datastackjobs']['data_stack_jobs_url']

    def request_page(self) -> str:
        """Request source html and access html text."""
        page = requests.get(self.url)
        html_contents: str = page.text
        return html_contents

    def parse_html_contents(self, html_contents: str) -> BeautifulSoup:
        """Use Beautiful Soup to parse html contents."""
        soup = BeautifulSoup(html_contents, "html.parser")
        return soup

    def access_job_data(self, soup: BeautifulSoup) -> list[dict]:
        """Pull contents from Datastackjobs.com-specific html tag and convert to python dict type via JSON library."""
        jobs_data = soup.find(name="script", id="__NEXT_DATA__")
        jobs_data: dict = json.loads(jobs_data.string)
        return jobs_data["props"]["pageProps"]["jobs"]

    def clean_string(self, description: str) -> str:
        clean = re.compile('<.*?>')
        return re.sub(clean, '', description)

    def clean_description_tags(self, jobs_data: list) -> list:
        """Remove html tags from description column contents."""
        jobs_data_clean = []
        for job in jobs_data:
            job["description"] = self.clean_string(job["description"])
            jobs_data_clean.append(job)
        return jobs_data_clean

    def write_to_csv(self, jobs_data_clean: list) -> None:
        """Write jobs data to csv file."""
        with open("app/etl/static/data/data_stack_jobs.csv", mode="w") as file:
            fieldnames = [
                "application_url_or_email",
                "category",
                "company_logo_url",
                "company_name",
                "company_slug",
                "company_twitter",
                "description",
                "id",
                "location",
                "location_type",
                "position",
                "published_at",
                "slug",
                "status",
                "tags",
                "type",
            ]
            csv_writer = csv.DictWriter(f=file, fieldnames=fieldnames)
            csv_writer.writeheader()
            for row in jobs_data_clean:
                csv_writer.writerow(row)

    def run_ETL(self):
        html_contents = self.request_page()
        soup = self.parse_html_contents(html_contents)
        jobs_data = self.access_job_data(soup)
        jobs_data_clean = self.clean_description_tags(jobs_data)
        self.write_to_csv(jobs_data_clean)

if __name__ == "__main__":
    scraper = DataStackJobsScraper(configs=configs)
    scraper.run_ETL()
