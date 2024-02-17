import os

def delete_database():
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print(f"База данных удалена.")
    else:
        print(f"Файл бд не существует.")

delete_database()