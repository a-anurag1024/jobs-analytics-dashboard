import mysql.connector as mysql 
from dataclasses import dataclass


@dataclass
class DBCreds:
    
    host: str
    port: str
    user: str
    password: str
    database: str
    

class DBConnector:
    def __init__(self, creds: DBCreds):
        self.creds = creds
        
        self.conn = mysql.connect(
            host=self.creds.host,
            port=self.creds.port,
            user=self.creds.user,
            password=self.creds.password,
            database=self.creds.database
        )