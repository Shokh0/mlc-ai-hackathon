from utils.config import DATABASE_PATH
import sqlite3
import os


def create_database():

    open('db.sqlite3', 'w')
    with sqlite3.connect('db.sqlite3') as c:
    
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT(50),
                        email TEXT(100),
                        hash_password TEXT(64) NOT NULL,
                        role INTEGER CHECK (role IN (1, 0))
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS topics (
                        id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        date TEXT
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS messages (
                        message_id INTEGER PRIMARY KEY,
                        topic_id INTEGER,
                        content TEXT NOT NULL,
                        FOREIGN KEY (topic_id) REFERENCES topics (id)
                    )''')

create_database()