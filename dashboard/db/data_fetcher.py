from datetime import datetime, date
import pandas as pd

from dashboard.db.connector import DBConnector, DBCreds

class DataFetcher:
    def __init__(self, creds: DBCreds):
        self.db = DBConnector(creds).conn


    def fetch_jobs_bw_dates(self, 
                            start_date: date, 
                            end_date: date) -> pd.DataFrame:
        #query = "SELECT entry_date, job_id, seniority_level, employment_type, job_function, industries FROM jobs WHERE entry_date BETWEEN '{}' AND '{}'".format(start_date, end_date)
        query = """
        SELECT j1.entry_date, j1.job_id, j1.seniority_level, j1.employment_type, j1.job_function, j1.industries, 
        j2.job_title, j2.company, j2.location FROM jobs j1
        JOIN scrolled_jobs j2 ON j1.job_id = j2.job_id
        WHERE j1.entry_date BETWEEN '{}' AND '{}'
        """.format(start_date, end_date)
        
        cursor = self.db.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["entry_date", "job_id", "seniority_level", "employment_type", "job_function", "industries",
                                         "job_title", "company", "location"])
        return df
    
    
    def fetch_skills_bw_dates(self,
                              start_date: date,
                              end_date: date) -> pd.DataFrame:
        query = """SELECT job_id, skill, skill_rank, cluster_id FROM skills_cluster_tag 
        WHERE job_id IN (SELECT job_id FROM jobs WHERE entry_date BETWEEN '{}' AND '{}')""".format(start_date, end_date)
        cursor = self.db.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=['job_id', 'skill','skill_rank', 'cluster_id'])
        return df
    
    
    def fetch_skill_clusters(self) -> pd.DataFrame:
        query = "SELECT cluster_id, cluster_tags, cluster_head_tag FROM skills_clusters"
        cursor = self.db.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=['cluster_id', 'cluster_tags', 'cluster_head_tag'])
        return df