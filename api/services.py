from back.utils.singleton import Singleton
from back.utils.usefull_func import hashPassword
from back.utils.temp_data import LocalStoreg
from back.database_handler import DataBase
from back.utils.config import config

from fastapi import Request
from .schemes import Schemes

from inference.model_wrapper import AiAssistant

import sqlite3
import copy

from datetime import datetime, date


db = DataBase()
ls = LocalStoreg()

class Services(Singleton):

    def init(self):
        super().__init__()
        ai_assitant = AiAssistant()
        self.chat = ai_assitant.create_chat()

    def __init__(self) -> None: ...

    def get_login(self, items: Schemes.LoginRequestDTO, request: Request) -> Schemes.LoginResponseDTO:
        gmail: str = items.gmail
        password: str = items.password
        all_gmails = db.getAllUsersGmail()
        if all_gmails != None:
            all_gmails = list(map(lambda x: x[0], all_gmails))

        if gmail not in all_gmails:
            status: bool = False
            return Schemes.LoginResponseDTO(status=status)
        
        new_hash_password = hashPassword(password)
        curent_hash_password = db.getPasswordFromLogin(gmail)
        
        if curent_hash_password != None:
            if new_hash_password != curent_hash_password[0]: 
                status: bool = False
                return Schemes.LoginResponseDTO(status=status)
            
            print(request.headers)
            user_name = db.getUserNameFromGmail(gmail)[0]
            login_id = db.getUser(gmail)[0]
            ls.updateName(login_id, user_name)
            host = request.headers.get('host')
            ls.updateUserId(host, login_id)
            status: bool = True
            return Schemes.LoginResponseDTO(status=status, url=f'{config.base_url}/edu-chat')
        status: bool = False
        return Schemes.LoginResponseDTO(status=status)

    def get_singup(items: Schemes.SingupRequestDTO, request: Request) -> Schemes.SingupResponseDTO:
        host = request.headers.get('host')
        login: str = items.login
        gmail: str = items.gmail
        password: str = items.password
        teacher_student_flag: int = items.teacher_student_flag
        all_gmails = db.getAllUsersGmail()
        
        if gmail in all_gmails:
            status: bool = False
            return Schemes.SingupResponseDTO(status=status)
        
        hash_password = hashPassword(password)
        db.addUser(login, hash_password, teacher_student_flag)
        status: bool = True
        return Schemes.SingupResponseDTO(status=status, url=f'{config.base_url}/edu-chat') 

    def get_lamini(self, question : Schemes.LaminiRequestDTO) -> Schemes.LaminiResponseDTO:
        res = self.chat.run(question.question)
        result = copy.deepcopy(res)
        print(result)
        status = True
        return Schemes.LaminiResponseDTO(status=status, message=result)
    
    def get_new_chat(self, items: Schemes.NewChatDataRequestDTO, request: Request) -> Schemes.NewChatDataResponseDTO:
        host = request.headers.get('host')
        user_id = ls.getUserId(host)
        ls.updateTopicId(user_id, None)
        status = True 
        return Schemes.NewChatDataResponseDTO(status=status)

    def get_user_id_and_topic_id(self, items: Schemes.UserIdAndTopicIdDataRequestDTO, request: Request) -> Schemes.UserIdAndTopicIdDataResponseDTO:
        host = request.headers.get('host')
        user_id = ls.getUserId(host)
        topic_id = ls.getTopicId(user_id)
        name = ls.getName(user_id)
        status = True
        return Schemes.UserIdAndTopicIdDataResponseDTO(status=status, user_id=user_id, topic_id=topic_id, login=name)

    def add_new_message(self, items: Schemes.AddMessagesRequestDTO, request: Request) -> Schemes.AddMessagesResponseDTO:
        topic_id = items.topic_id
        content = items.content
        is_ai = items.is_ai
        host = request.headers.get('host')
        user_id = ls.getUserId(host)
        ls.updateTopicId(user_id, topic_id)
        # print(topic_id, content, is_ai)
        db.addMessage(topic_id, user_id, content, is_ai)
        status: bool = True
        return Schemes.AddMessagesResponseDTO(status=status)
    
    def get_messages(self, items: Schemes.GetMessagesRequestDTO, request: Request) -> Schemes.GetMessagesResponseDTO:
        topic_id: int = items.topic_id
        user_id: int = items.user_id
        # print(topic_id, user_id)
        messages = db.getMessagesFromTopicIdAndUserId(topic_id, user_id)
        status: bool = True
        return Schemes.GetMessagesResponseDTO(status=status, messages=messages)
    
    def add_topic(self, items: Schemes.AddTopicRequestDTO, request: Request) -> Schemes.AddTopicResponseDTO:
        user_id = items.user_id
        title = items.title
        date = datetime.now().strftime('%d.%m.%Y %H:%M')
        row = db.addTopic(user_id, title, date)
        topic_id = row[0]
        host = request.headers.get('host')
        user_id = ls.getUserId(host)
        ls.updateTopicId(user_id, topic_id)
        # print('topic_id', row[0])
        status: bool = True
        return Schemes.AddTopicResponseDTO(status=status, topic_id=topic_id)
    
    def get_topics(self, items: Schemes.GetTopicsRequestDTO, request: Request) -> Schemes.GetTopicsResponseDTO:
        login_id = items.login_id
        with sqlite3.connect(config.DATABASE_PATH) as c:
            topics = c.execute(f"""SELECT * FROM topics WHERE user_id = '{login_id}'""").fetchall()

        status: bool = True
        return Schemes.GetTopicsResponseDTO(status=status, topics=topics)

    def del_topic(self, items: Schemes.DelTopicRequestDTO, request: Request) -> Schemes.DelTopicResponseDTO:
        topic_id = items.topic_id
        with sqlite3.connect(config.DATABASE_PATH) as c:
            c.execute(f"""DELETE FROM messages WHERE topic_id = '{topic_id}'""")
            c.execute(f"""DELETE FROM topics WHERE id = '{topic_id}'""")

        status: bool = True
        return Schemes.DelTopicResponseDTO(status=status)


























