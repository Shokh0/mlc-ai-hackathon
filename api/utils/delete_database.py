import os

# run from "api" directory
def delete_database():
    try:
        if os.path.exists('../db.sqlite3'):
            os.remove('../db.sqlite3')
            print(f"База данных удалена.")
        else:
            print(f"Файл бд не существует.")
    except Exception as e:
        print(f'[ERROR] {e}')

delete_database()