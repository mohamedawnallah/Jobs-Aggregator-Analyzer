class IndeedJobSkillsTransformer(Transformer):
    """Indeed Full Job Info Transformer Abstract Class"""
    @staticmethod
    def transform(job_skills: str) -> str:
        """Transform Full Job Info"""
        job_skills: str = job_skills.strip()
        return job_skills

    @staticmethod
    def get_job_skills(all_job_skills: List[str], job_description: str) -> str:
        """Extract Job Skills from job description"""
        job_skills_found: str = Utils.get_all_found_words(all_job_skills,job_description)
        global i
        i += 1
        print("Job Skills Found: ", job_skills_found, "In the Row: ", i)
        
        return job_skills_found