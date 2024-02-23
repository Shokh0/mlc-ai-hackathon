from config import DATABASE_PATH
import sqlite3
import os

# run from "api" directory

def create_database():

    try:
        open('../db.sqlite3', 'w')
        with sqlite3.connect('../db.sqlite3') as c:
        
            c.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            login TEXT(150),
                            hash_password TEXT(64) NOT NULL,
                            role INTEGER CHECK (role IN (1, 0))
                        )''')

            c.execute('''CREATE TABLE IF NOT EXISTS topics (
                            id INTEGER PRIMARY KEY,
                            user_id INTEGER,
                            title TEXT NOT NULL,
                            date TEXT,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )''')

            c.execute('''CREATE TABLE IF NOT EXISTS messages (
                            message_id INTEGER PRIMARY KEY,
                            topic_id INTEGER,
                            content TEXT NOT NULL,
                            FOREIGN KEY (topic_id) REFERENCES topics (id)
                        )''')
    except Exception as e:
        print(f'[ERROR] {e}')
create_database()