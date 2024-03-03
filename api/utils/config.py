import os


class Config:

    port:          int = 80
    local:         str = '127.0.0.1'
    external:      str = '26.142.248.33'
    base_url:      str = f'http://{local}:{port}'  
    DATABASE_PATH: str = os.getcwd().replace("\\api\\utils", "").replace("\\", "/")+"/api/db.sqlite3"

config = Config()