from utils.singleton import Singleton
from utils.config import DATABASE_PATH
import sqlite3


class DataBase(Singleton):
    
    def init(self):
        super().__init__()
        self.db_path = DATABASE_PATH

    
    def addUser(self, login, hash_password: str, role: int[1 | 0]):
        with sqlite3.connect(self.db_path) as c:
            c.execute('INSERT INTO users (login, hash_password, role) VALUES (?, ?, ?, ?)', (login, hash_password, role))
            c.commit()
            print(f'[INFO] new user "{login}" has been added')
    
    def getUser(self, login: str):
        with sqlite3.connect(self.db_path) as c:
            user_info = c.execute('SELECT * FROM users WHERE login = ?', (login,))
            return user_info

    def getPasswordFromLogin(self, login: str):
        with sqlite3.connect(self.db_path) as c:
            hash_password = c.execute('SELECT hash_password FROM users WHERE login = ?', (login,))
            return hash_password
        
    def addTopic(self, title: str, date: str): 
        with sqlite3.connect(self.db_path) as c:
            c.execute('INSERT INTO topics (title, date) VALUES (?, ?)', (title, date))
            c.commit()
        
    def getTopic(self, user_id: str): 
        with sqlite3.connect(self.db_path) as c:
            topics = c.execute('SELECT * FROM topics WHERE user_id = ?', (user_id,))
            return topics

    def addMessage(self, topic_id: int, content: str): 
        with sqlite3.connect(self.db_path) as c:
            c.execute('INSERT INTO messages (topic_id, content) VALUES (?, ?)', (topic_id, content))
            c.commit()

    def getMessagesFromTopicId(self, topic_id: int): 
        with sqlite3.connect(self.db_path) as c:
            c.execute('SELECT * FROM messages WHERE topic_id = ?' (topic_id,))
            c.commit()



