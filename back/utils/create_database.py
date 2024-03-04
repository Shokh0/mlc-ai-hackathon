from config import config
import sqlite3
import os

# run from "api" directory

def create_database():

    try:
        open(config.DATABASE_PATH, 'w')
        with sqlite3.connect(config.DATABASE_PATH) as c:
        
            c.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            login TEXT(150),
                            gmail STRING(200),
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
                            user_id INTEGER,
                            content TEXT NOT NULL,
                            is_ai INTEGER CHECK (is_ai IN (1, 0)),
                            FOREIGN KEY (topic_id) REFERENCES topics (id),
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )''')
    except Exception as e:
        print(f'[ERROR] {e}')
create_database()