from .utils.singleton import Singleton
from .utils.config import config
import sqlite3


class DataBase(Singleton):
    
    def init(self):
        super().__init__()
        self.db_path = config.DATABASE_PATH

    # users
    def addUser(self, login: str, gmail: str, hash_password: str, role: int):
        with sqlite3.connect(self.db_path) as c:
            c.execute('INSERT INTO users (login, gmail hash_password, role) VALUES (?, ?, ?, ?)', (login, gmail, hash_password, role))
            c.commit()
            print(f'[INFO] new user "{login}" has been added')
    
    def getUser(self, gmail: str):
        with sqlite3.connect(self.db_path) as c:
            user_info = c.execute('SELECT * FROM users WHERE gmail = ?', (gmail,)).fetchone()
            return user_info
    
    def getUserNameFromGmail(self, gmail: str):
        with sqlite3.connect(self.db_path) as c:
            user_name = c.execute("SELECT login FROM users WHERE gmail = ?", (gmail,)).fetchone()
            return user_name

    def getPasswordFromLogin(self, gmail: str):
        with sqlite3.connect(self.db_path) as c:
            hash_password = c.execute('SELECT hash_password FROM users WHERE gmail = ?', (gmail,)).fetchone()
            return hash_password

    def getAllUsersGmail(self):
        with sqlite3.connect(self.db_path) as c:
            gmails = c.execute('SELECT gmail FROM users').fetchall()
            return gmails
        
    def getAllPasswords(self):
        with sqlite3.connect(self.db_path) as c:
            hash_passwords = c.execute('SELECT hash_password FROM users').fetchall()
            return hash_passwords

    

    # Assistant
    def addTopic(self, user_id: int, title: str, date: str): 
        with sqlite3.connect(self.db_path) as c:
            cursor = c.cursor()
            cursor.execute('INSERT INTO topics (user_id, title, date) VALUES (?, ?, ?)', (user_id, title, date)).fetchone()
            last_row_id = cursor.lastrowid
            c.commit()
            print("ID последней вставленной строки:", last_row_id)
            row = c.execute(f"""SELECT * FROM topics WHERE id = '{last_row_id}'""").fetchone()
            return row
            
    def getTopicsFromUserId(self, user_id: str): 
        with sqlite3.connect(self.db_path) as c:
            topics = c.execute('SELECT * FROM topics WHERE user_id = ?', (user_id,)).fetchall()
            return topics

    def addMessage(self, topic_id: int, user_id: int, content: str, is_ai: int): 
        with sqlite3.connect(self.db_path) as c:
            c.execute('INSERT INTO messages (topic_id, user_id, content, is_ai) VALUES (?, ?, ?, ?)', (topic_id, user_id, content, is_ai))
            c.commit()

    def getMessagesFromTopicIdAndUserId(self, topic_id: int, user_id: int): 
        with sqlite3.connect(self.db_path) as c:
            messages = c.execute('SELECT * FROM messages WHERE topic_id = ? AND user_id = ?', (topic_id, user_id)).fetchall()
            print(messages)
            return messages


