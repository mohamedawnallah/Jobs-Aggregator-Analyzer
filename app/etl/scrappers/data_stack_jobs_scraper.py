"""Python script to scrape Datastackjobs.com for job postings.

Datastackjobs.com is a simple job board that displays job postings around the world.

This script automates the process of scraping Datastackjobs.com for job postings
and saves the results in a CSV file(temporary).
"""

import csv
import json
import requests
from bs4 import BeautifulSoup
from html_tags import html_tags


class DataStackJobsScraper:
    """Scraper for Datastackjobs.com"""

    def __init__(self):
        self.url = configs['datastackjobs']['data-stack_jobs_url']
        self.html_contents = self.request_page()
        self.soup = self.parse_html_contents()
        self.jobs_data = self.access_job_data()
        self.clean_description_tags()
        self.write_to_csv()

    def request_page(self):
        """Request source html and access html text."""
        page = requests.get(self.url)
        html_contents = page.text
        return html_contents

    def parse_html_contents(self):
        """Use Beautiful Soup to parse html contents."""
        soup = BeautifulSoup(self.html_contents, "html.parser")
        return soup

    def access_job_data(self):
        """Pull contents from Datastackjobs.com-specific html tag and convert to python dict type via JSON library."""
        jobs_data = self.soup.find(name="script", id="__NEXT_DATA__")
        jobs_data = json.loads(jobs_data.string)
        return jobs_data["props"]["pageProps"]["jobs"]

    def clean_description_tags(self):
        """Remove html tags from description column contents."""
        cleaned_jobs = []
        for job in self.jobs_data:
            description = job["description"]
            for tag in html_tags:
                if tag in description:
                    description = description.replace(tag, "")
            job["description"] = description
            cleaned_jobs.append(job)
        self.jobs_data = cleaned_jobs

    def write_to_csv(self):
        """Write jobs data to csv file."""
        with open("app/static/data/data_stack_jobs.csv", mode="w") as file:
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
            for row in self.jobs_data:
                csv_writer.writerow(row)


if __name__ == "__main__":
    scraper = DataStackJobsScraper()
