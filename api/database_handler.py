<<<<<<< HEAD
from .utils.singleton import Singleton
from .utils.config import DATABASE_PATH
import sqlite3


class DataBase(Singleton):
    
    def init(self):
        super().__init__()
        self.db_path = DATABASE_PATH

    # users
    def addUser(self, login, hash_password: str, role: int):
        with sqlite3.connect(self.db_path) as c:
            c.execute('INSERT INTO users (login, hash_password, role) VALUES (?, ?, ?, ?)', (login, hash_password, role))
            c.commit()
            print(f'[INFO] new user "{login}" has been added')
    
    def getUser(self, login: str):
        with sqlite3.connect(self.db_path) as c:
            user_info = c.execute('SELECT * FROM users WHERE login = ?', (login,)).fetchone()
            return user_info

    def getPasswordFromLogin(self, login: str):
        with sqlite3.connect(self.db_path) as c:
            hash_password = c.execute('SELECT hash_password FROM users WHERE login = ?', (login,)).fetchone()
            return hash_password[0]

    def getAllUsersLogin(self):
        with sqlite3.connect(self.db_path) as c:
            logins = c.execute('SELECT login FROM users').fetchall()
            return logins
        
    def getAllPasswords(self):
        with sqlite3.connect(self.db_path) as c:
            hash_passwords = c.execute('SELECT hash_password FROM users').fetchall()
            return hash_passwords

    

    # Assistant
    def addTopic(self, user_id: int, title: str, date: str): 
        with sqlite3.connect(self.db_path) as c:
            c.execute('INSERT INTO topics (user_id, title, date) VALUES (?, ?, ?)', (user_id, title, date))
            c.commit()
        
    def getTopicsFromUserId(self, user_id: str): 
        with sqlite3.connect(self.db_path) as c:
            topics = c.execute('SELECT * FROM topics WHERE user_id = ?', (user_id,)).fetchall()
            return topics

    def addMessage(self, topic_id: int, content: str): 
        with sqlite3.connect(self.db_path) as c:
            c.execute('INSERT INTO messages (topic_id, content) VALUES (?, ?)', (topic_id, content))
            c.commit()

    def getMessagesFromTopicId(self, topic_id: int): 
        with sqlite3.connect(self.db_path) as c:
            c.execute('SELECT * FROM messages WHERE topic_id = ?' (topic_id,)).fetchall()
            c.commit()



=======
from .utils.singleton import Singleton
from .utils.config import DATABASE_PATH
import sqlite3


class DataBase(Singleton):
    
    def init(self):
        super().__init__()
        self.db_path = DATABASE_PATH

    # users
    def addUser(self, login, hash_password: str, role: int):
        with sqlite3.connect(self.db_path) as c:
            c.execute('INSERT INTO users (login, hash_password, role) VALUES (?, ?, ?)', (login, hash_password, role))
            c.commit()
            print(f'[INFO] new user "{login}" has been added')
    
    def getUser(self, login: str):
        with sqlite3.connect(self.db_path) as c:
            user_info = c.execute('SELECT * FROM users WHERE login = ?', (login,)).fetchone()
            return user_info

    def getPasswordFromLogin(self, login: str):
        with sqlite3.connect(self.db_path) as c:
            hash_password = c.execute('SELECT hash_password FROM users WHERE login = ?', (login,)).fetchone()
            return hash_password

    def getAllUsersLogin(self):
        with sqlite3.connect(self.db_path) as c:
            logins = c.execute('SELECT login FROM users').fetchall()
            return logins
        
    def getAllPasswords(self):
        with sqlite3.connect(self.db_path) as c:
            hash_passwords = c.execute('SELECT hash_password FROM users').fetchall()
            return hash_passwords

    

    # Assistant
    def addTopic(self, user_id: int, title: str, date: str): 
        with sqlite3.connect(self.db_path) as c:
            c.execute('INSERT INTO topics (user_id, title, date) VALUES (?, ?, ?)', (user_id, title, date))
            c.commit()
        
    def getTopicsFromUserId(self, user_id: str): 
        with sqlite3.connect(self.db_path) as c:
            topics = c.execute('SELECT * FROM topics WHERE user_id = ?', (user_id,)).fetchall()
            return topics

    def addMessage(self, topic_id: int, content: str): 
        with sqlite3.connect(self.db_path) as c:
            c.execute('INSERT INTO messages (topic_id, content) VALUES (?, ?)', (topic_id, content))
            c.commit()

    def getMessagesFromTopicId(self, topic_id: int): 
        with sqlite3.connect(self.db_path) as c:
            messages = c.execute('SELECT * FROM messages WHERE topic_id = ?' (topic_id,)).fetchall()
            return messages


>>>>>>> ecd7761f473415b6450b959cf902accbfd58077b
