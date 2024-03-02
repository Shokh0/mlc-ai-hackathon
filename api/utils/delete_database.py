from config import config
import os


# run from "api" directory
def delete_database():
    try:
        if os.path.exists(config.DATABASE_PATH):
            os.remove(config.DATABASE_PATH)
            print(f"База данных удалена.")
        else:
            print(f"Файл бд не существует.")
    except Exception as e:
        print(f'[ERROR] {e}')

delete_database()