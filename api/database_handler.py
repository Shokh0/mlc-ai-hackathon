from utils.singleton import Singleton
from utils.config import DATABASE_PATH
import sqlite3


class DataBase(Singleton):
    
    def init(self):
        super().__init__()
        self.db_path = DATABASE_PATH

    
    
