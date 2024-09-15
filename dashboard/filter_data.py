import pandas as pd

class FilterDBs:
    def __init__(self, 
                 jobs_db: pd.DataFrame,
                 skills_db: pd.DataFrame):
        self.jobs_db = jobs_db
        self.skills_db = skills_db
        
        self.filters = {'Seniority Level': self.filter_seniority_level,
                        'Employment Type': self.filter_employment_type,
                        'Job Function': self.filter_job_function,
                        'Industries': self.filter_industries}
    
    
    def filter_skills_db(self, jobs_db: pd.DataFrame) -> pd.DataFrame:
        """
        Update the skills_db based on filtered jobs_db
        """
        return self.skills_db[self.skills_db['job_id'].isin(jobs_db['job_id'])]
    
    
    def filter_jobs_db(self, filters: dict) -> pd.DataFrame:
        """
        Update the jobs_db based on filters
        """
        jobs_db = self.jobs_db.copy()
        for k, func in self.filters.items():
            jobs_db = func(jobs_db, filter_values=filters[k])
        return jobs_db
    
    
    def filter_seniority_level(self, jobs_db: pd.DataFrame, filter_values: list) -> pd.DataFrame:
        if "All" in filter_values or len(filter_values) == 0:
            return jobs_db
        return jobs_db[jobs_db['seniority_level'].isin(filter_values)]
    
    
    def filter_employment_type(self, jobs_db: pd.DataFrame, filter_values: list) -> pd.DataFrame:
        if "All" in filter_values or len(filter_values) == 0:
            return jobs_db
        return jobs_db[jobs_db['employment_type'].isin(filter_values)]
    
    
    def filter_job_function(self, jobs_db: pd.DataFrame, filter_values: list) -> pd.DataFrame:
        if "All" in filter_values or len(filter_values) == 0:
            return jobs_db
        return jobs_db[jobs_db['job_function'].isin(filter_values)]
    
    
    def filter_industries(self, jobs_db: pd.DataFrame, filter_values: list) -> pd.DataFrame:
        if "All" in filter_values or len(filter_values) == 0:
            return jobs_db
        return jobs_db[jobs_db['industries'].isin(filter_values)]
    
    
    def get_filtered_dbs(self, filters: dict) -> tuple:
        jobs_db = self.filter_jobs_db(filters)
        skills_db = self.filter_skills_db(jobs_db)
        return jobs_db, skills_db
    
    
    def get_options(self, 
                    column: str,
                    include_all: bool = True) -> list:
        opts = list(self.jobs_db.groupby([column]).agg({'job_id': 'count'}).reset_index().sort_values(by='job_id', ascending=False)[column].values)
        if include_all:
            opts = ["All"] + opts
        return opts