from utils.config import DATABASE_PATH
import os


# run from "api" directory
def delete_database():
    try:
        if os.path.exists(DATABASE_PATH):
            os.remove(DATABASE_PATH)
            print(f"База данных удалена.")
        else:
            print(f"Файл бд не существует.")
    except Exception as e:
        print(f'[ERROR] {e}')

delete_database()