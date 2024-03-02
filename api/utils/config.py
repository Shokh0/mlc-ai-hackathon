import os


class Config:

    base_url = 'http://127.0.0.1:80' #'http://26.142.248.33:80' 
    DATABASE_PATH = os.getcwd().replace("\\api\\utils", "").replace("\\", "/")+"/api/db.sqlite3"


config = Config()