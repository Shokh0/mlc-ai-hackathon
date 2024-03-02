import os


class Config:

    local_url = 'http://127.0.0.1:80'
    external_url = 'http://26.142.248.33:80'
    base_url = local_url  
    DATABASE_PATH = os.getcwd().replace("\\api\\utils", "").replace("\\", "/")+"/api/db.sqlite3"


config = Config()