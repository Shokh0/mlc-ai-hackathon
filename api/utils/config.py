import os
base_path = os.getcwd().replace("\\api\\utils", "").replace("\\", "/")
DATABASE_PATH = base_path+"/api/db.sqlite3"
print(DATABASE_PATH)