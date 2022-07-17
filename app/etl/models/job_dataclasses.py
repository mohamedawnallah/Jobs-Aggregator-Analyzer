from collections import namedtuple
from dataclasses import is_dataclass
from dataclasses import dataclass, make_dataclass
from etl.utils.utils import Utils

CONFIGS: dict = Utils.get_configs()

_job_info_attrs = Utils.get_value_of_key_from_dict(CONFIGS, "job")
_job_basic_info_attrs = Utils.get_value_of_key_from_dict(_job_info_attrs, "job_basic_info").keys()
JobBasicInfo: dataclass = make_dataclass('JobBasicInfo', _job_basic_info_attrs, frozen=True,)

_company_basic_info_attrs = Utils.get_value_of_key_from_dict(CONFIGS, "company").keys()
CompanyBasicInfo: dataclass = make_dataclass('CompanyBasicInfo', _company_basic_info_attrs)

_job_info_attrs = Utils.get_value_of_key_from_dict(CONFIGS, "job")
_job_more_info_attrs = Utils.get_value_of_key_from_dict(_job_info_attrs, "job_more_info").keys()
JobMoreInfo: dataclass = make_dataclass('JobMoreInfo', _job_more_info_attrs, frozen=True)

@dataclass
class Country:
    """Company Data Class"""
    country_name: str
    country_code: str

@dataclass(frozen=True)
class JobCompanyBasicInfo:
    """JobCompanyBasicInfo Data class"""
    job_basic_info: JobBasicInfo
    company_basic_info: CompanyBasicInfo


@dataclass(frozen=True)
class JobFullInfo:
    """Job Full Info Data class"""
    job_basic_info: JobBasicInfo
    job_more_info: JobMoreInfo
    company_basic_info: CompanyBasicInfo
    job_skills: dict

    def to_dict(self):
        """Convert to dict"""
        job_full_info: dict=  {
            **vars(self.job_basic_info),
            **vars(self.company_basic_info),
            **vars(self.job_more_info),
            **self.job_skills
        }
        return job_full_info
