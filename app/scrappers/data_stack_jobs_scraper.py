"""Python script to scrape Datastackjobs.com for job postings.

Datastackjobs.com is a simple job board that displays job postings around the world.

This script automates the process of scraping Datastackjobs.com for job postings
and saves the results in a CSV file(temporary).
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


html_tags = ['<p>', '<h1>', '<h2>', '<h3>', '<h4>', '<h5>', '<h6>', '<strong>', '<em>', '<abbr>', '<address>',
             '<bdo>', '<blockquote>', '<cite>', '<q>', '<code>', '<ins>', '<del>', '<dfn>', '<kbd>', '<pre>',
             '<samp>', '<var>', '<br>', '<div>', '<a>', '<base>', '<img>', '<area>', '<map>', '<param>', '<object>',
             '<ul>', '<ol>', '<li>', '<dl>', '<dt>', '<dd>', '</p>', '</h1>', '</h2>', '</h3>', '</h4>', '</h5>',
             '</h6>', '</strong>', '</em>', '</abbr>', '</address>', '</bdo>', '</blockquote>', '</cite>', '</q>',
             '</code>', '</ins>', '</del>', '</dfn>', '</kbd>', '</pre>', '</samp>', '</var>', '</br>', '</div>',
             '</a>', '</base>', '</img>', '</area>', '</map>', '</param>', '</object>', '</ul>', '</ol>', '</li>',
             '</dl>', '</dt>', '</dd>', '<br />']

html_artifacts = []

URL = 'https://datastackjobs.com'
page = requests.get(URL)
contents = page.text
soup = BeautifulSoup(contents, "html.parser")
results = soup.find(name='script', id="__NEXT_DATA__")
data = json.loads(results.string)
jobs = data['props']['pageProps']['jobs']


def clean_description_tags(description: str) -> str:
    '''Remove html tags from description column contents'''
    for tag in html_tags:
        if tag in description:
            description = description.replace(tag, "")
    return description


df = pd.DataFrame(jobs)
df['description'] = [clean_description_tags(x) for x in df['description']]
df.to_csv('app/static/data/data_stack_jobs.csv', index=False)




# Generate a list of job search terms
# How are search terms are included in URL?
# What is the structure of the main page?
# How are multiple pages represented in URL?
# What HTML tags are used for job postings on the main page?
# What HTML tags are used for different sections of the individual job posting page?
