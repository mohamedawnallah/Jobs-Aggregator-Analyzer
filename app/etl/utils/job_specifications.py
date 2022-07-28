from collections import defaultdict
from typing import Optional, Union, Any
from abc import abstractmethod, ABC
from utils.utils import Utils


class BaseSpecification:
    """Base Class for Specification"""

    @abstractmethod
    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if the candidate is satisfied by the specification"""

    def __or__(self, other):
        """Overriding or operator for AndSpecification"""
        return OrSpecification(self, other)


class OrSpecification(BaseSpecification):
    """And Specification for Base Specification class"""

    def __init__(self, *args):
        self.args = args

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        for spec in self.args:
            spec_generator = spec.is_satisfied_by(candidate)
            for job_spec_dict in spec_generator:
                yield job_spec_dict


class ProgrammingLanguagesSpecification(BaseSpecification):
    """Programming Languages Specification"""

    def __init__(
        self, configs: dict, job_specs: Optional[str] = "programming_languages"
    ):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if programming languages provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class DBEnginesSpecification(BaseSpecification):
    """DB Engines Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "db_engines"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if DB engines provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class SQLSpecification(BaseSpecification):
    """SQL Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "sql_and_no_sql"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if SQL provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class IngestSassSpecification(BaseSpecification):
    """Ingest SAS Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "ingest_sass"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if Ingest SAS provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class IngestTechSpecification(BaseSpecification):
    """Ingest Tech Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "ingest_tech"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if Ingest Tech provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class ObjectStorageSpecification(BaseSpecification):
    """Object Storage Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "object_storage"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if Object Storage provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class CloudProvidersSpecification(BaseSpecification):
    """Cloud Providers Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "cloud_providers"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if Cloud Providers provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class MetaStoreSpecification(BaseSpecification):
    """Meta Store Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "metastore"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if MetaStore provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class OpenTableFormatsSpecification(BaseSpecification):
    """Open Table Formats Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "open_table_formats"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        "Check if Open Table Formats provided in configs file statisfied in the candidate(job description)"
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class ComputeSpecification(BaseSpecification):
    """Compute Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "compute"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if Compute provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class AnalyticsEngineSpecification(BaseSpecification):
    """Analytics Engine Specification"""
    def __init__(self, configs: dict, job_specs: Optional[str] = "analytics_engine"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if Analytics Engine provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class DataVizToolsSpecification(BaseSpecification):
    """Data Viz Tools Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "data_viz_tools"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Data Viz Tools Specification"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class GitForDataSpecification(BaseSpecification):
    """Git for Data Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "git_for_data"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if Git for Data provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class OrcherstrationSpecification(BaseSpecification):
    """Orchestration Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "orcherstration"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if Orchestration provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class MlopsEndtoEndSpecification(BaseSpecification):
    """MLOps End to End Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "mlops_end_to_end"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if MLOps End to End provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class DataCentricAIMLSpecification(BaseSpecification):
    """Data Centric AIML Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "data_centric_ai_ml"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if Data Centric AI/ML provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class AnalyticsWorkflowSpecification(BaseSpecification):
    """Analytics Workflow Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "analytics_workflow"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if Analytics Workflow provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class MLObservabilitySpecification(BaseSpecification):
    """ML Observability Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "ml_observability"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if ML Observability provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class NotebooksSpecification(BaseSpecification):
    """Notebooks Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "notebooks"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if Notebooks provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class FeatureStoresSpecification(BaseSpecification):
    """Feature Stores Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "feature_stores"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if Feature Stores provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class DiscoveryGovernanceSpecification(BaseSpecification):
    """Discovery Governance Specification"""

    def __init__(
        self, configs: dict, job_specs: Optional[str] = "discovery_governance"
    ):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if Discovery Governance provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class DevopsSpecification(BaseSpecification):
    """Devops Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "devops"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if Devops provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )


class AutomationSpecification(BaseSpecification):
    """Automation Specification"""

    def __init__(self, configs: dict, job_specs: Optional[str] = "automation"):
        self.job_specs = job_specs
        self.job_specs_values = Utils.get_value_of_key_from_dict(configs, self.job_specs)

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        """Check if Automation provided in configs file statisfied in the candidate(job description)"""
        return Utils.is_job_spec_satisfied(
            self.job_specs_values, self.job_specs, candidate
        )

class BachelorComputerScienceSpecification(BaseSpecification):
    """Computer Science Bachelor Degree Specification"""

    def __init__(self, job_spec: Optional[str] = "bachelor of computer science", degree_filter: Optional[list[str]] = None):
        if degree_filter is None:
            degree_filter = ["bachelor","computer science"]
        self.job_spec = job_spec
        self.degree_filter = degree_filter

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        return Utils.is_degree_filter_satisfied(self.job_spec,self.degree_filter, candidate)

class MasterComputerScienceSpecification(BaseSpecification):
    """Computer Science Master Degree Specification"""

    def __init__(self, job_spec: Optional[str] = "master of computer science", degree_filter: Optional[list[str]] = None):
        if degree_filter is None:
            degree_filter = ["master","computer science"]
        self.job_spec = job_spec
        self.degree_filter = degree_filter

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        return Utils.is_degree_filter_satisfied(self.job_spec,self.degree_filter, candidate)

class PHDComputerScienceSpecification(BaseSpecification):
    """Computer Science PHD Degree Specification"""

    def __init__(self, job_spec: Optional[str] = "phd of computer science", degree_filter: Optional[list[str]] = None):
        if degree_filter is None:
            degree_filter = ["phd","computer science"]
        self.job_spec = job_spec
        self.degree_filter = degree_filter

    def is_satisfied_by(self, candidate: Any) -> Union[bool, Any]:
        return Utils.is_degree_filter_satisfied(self.job_spec,self.degree_filter, candidate)


class Filter(ABC):
    """Base Filter Class"""
    @staticmethod
    @abstractmethod
    def filter(spec: BaseSpecification, job_description: str) -> dict:
        """Filter the job description based on given specification"""


class JobDescriptionFilter(Filter):
    """Filter the job description based on the spec"""
    @staticmethod
    def filter(spec: BaseSpecification, job_description: str = "") -> dict[str, str]:
        """Filter the job description based on the spec"""
        if not isinstance(spec, BaseSpecification):
            raise TypeError("spec must be an instance of BaseSpecification")
        is_satisfied_generator = spec.is_satisfied_by(job_description)
        job_skills_list = list(is_satisfied_generator)
        all_job_skills = defaultdict(str)
        for job_skill in job_skills_list:
            first_job_spec_key = next(iter(job_skill))
            if (
                first_job_spec_key not in all_job_skills
                or job_skill[first_job_spec_key] != "N/A"
            ):
                all_job_skills[first_job_spec_key] += (
                    job_skill[first_job_spec_key] + ", "
                )

        if not job_description:
            return list(all_job_skills)
        return dict(all_job_skills)

    @staticmethod
    def get_job_skills_list(job_specfications: OrSpecification) -> list[str]:
        """Get the job skills list from the job specifications"""
        if not isinstance(job_specfications, BaseSpecification):
            raise TypeError("job_specfications must be an instance of OrSpecification")
        job_skills: list = JobDescriptionFilter.filter(job_specfications)
        return job_skills