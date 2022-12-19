import csv
import json

from loguru import logger
from app.utilities import decorators
from common.etls_common import CSVPersistenceManager
from typing import Iterator
from pipeline.utilities.utils import Utils
from models.job_model import JobFullInfo

class IndeedPersistenceManager(CSVPersistenceManager):
    """Persistence manager class"""
    @staticmethod
    @decorators.timer
    def write_to_csv(
        csv_file_name: str,
        jobs_countries_gen: Iterator[JobFullInfo]
    ) -> bool:
        """Write data to csv file"""
        with open(csv_file_name, "w", encoding="utf-8") as csv_file:
            job_item = {}
            for index, job_full_info in enumerate(jobs_countries_gen):
                job_dict = job_full_info.to_dict()
                if index == 0 and not job_item:
                    job_item = job_dict
                    csv_writer = csv.DictWriter(csv_file, fieldnames=job_item.keys())
                    csv_writer.writeheader()
                are_all_job_skills_null = Utils.are_all_job_skills_null(job_full_info.job_skills)
                if not are_all_job_skills_null:
                    csv_writer.writerow(job_dict)
        return True
