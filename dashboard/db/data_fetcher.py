from datetime import datetime, date
import pandas as pd

from dashboard.db.connector import DBConnector, DBCreds

class DataFetcher:
    def __init__(self, creds: DBCreds):
        self.db = DBConnector(creds).conn

    def fetch_data_bw_dates(self, 
                            start_date: date, 
                            end_date: date) -> pd.DataFrame:
        query = "SELECT entry_date, job_id, seniority_level, employment_type, job_function, industries FROM jobs WHERE entry_date BETWEEN '{}' AND '{}'".format(start_date, end_date)
        cursor = self.db.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["entry_date", "job_id", "seniority_level", "employment_type", "job_function", "industries"])
        return df