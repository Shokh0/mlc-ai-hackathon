import sqlite3
from schemes import LoginRequestDTO, LoginResponseDTO

class Services:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("your_database.db")  
        self.cursor = self.conn.cursor()

    def get_login(self, login, password, flag):
        query = "SELECT login, hash_password, role FROM users WHERE login = ? AND hash_password = ? AND role = ?"
        self.cursor.execute(query, (login, password, flag))

        result = self.cursor.fetchone()

        if result:
            return LoginResponseDTO(response=True)  # user found
        else:
            return LoginResponseDTO(response=False)  # user not found

    def __del__(self):
        self.conn.close()
