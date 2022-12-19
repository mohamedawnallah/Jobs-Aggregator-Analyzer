from typing import List
import re
from pipeline.common.transformers_common import Transformer

class LightCastJobSkillsTransformer(Transformer):
    """Indeed Basic Job Info Transformer"""
    @staticmethod
    def transform(job_skills: List[dict]) -> str:
        """Transform the basic job company info to a namedtuple"""
        job_skills_transformed: str = LightCastJobSkillsTransformer._get_valid_job_skills(job_skills)
        return job_skills_transformed

    @staticmethod
    def _get_valid_job_skills(all_job_skills: List[dict]) -> str:
        """Get the valid job skills"""
        job_skills: str = set()
        for job_skill in all_job_skills:
            skill_name = job_skill["name"].lower().strip()
            skill_name = re.escape(skill_name)
            job_skills.add(skill_name)
        job_skills: List[str] = list(job_skills)
        return job_skills

