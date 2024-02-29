from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from flask import request
from pydantic import BaseModel
from typing import Union
from starlette.responses import JSONResponse
from api.api_services.schemes import *
from api.database_handler import *
from api.utils.usefull_func import hashPassword
from inference.model_wrapper import AiAssistant
import copy
import sqlite3

"""This module includes main method for working with AI assistant model."""


ai_assitant = AiAssistant()
chat = ai_assitant.create_chat()

class LocalStoreg:

    def __init__(self):
        self.user_id = {}
        self.topic_id = {}

    def updateUserId(self, host, user_id):
        self.user_id.update({host: user_id})    
    
    def getUserId(self, host):
        user_id = self.user_id.get(host, None)
        print('user_id: ', user_id)
        return user_id
    
    def updateTopicId(self, user_id, topic_id):
        self.user_id.update({user_id: topic_id})
    
    def getTopicId(self, user_id):
        topic_id = self.user_id.get(user_id, None)
        print('topic_id: ', topic_id)
        return topic_id


app = FastAPI(
    title="Inference API for Lamini-77M",
    description="A simple API that use MBZUAI/LaMini-Flan-T5-77M as a chatbot",
    version="1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

db = DataBase()
ls = LocalStoreg()

@app.get("/")
def read_root() -> JSONResponse:
    return JSONResponse({"message": "Hello, World"})

@app.get('/d')
async def readDocsApi() -> RedirectResponse: 
    return RedirectResponse(f"/docs")

@app.get('/r')
async def readRedocApi() -> RedirectResponse: 
    return RedirectResponse(f"/redoc")

@app.post('/api/lamini')
async def lamini(question : LaminiRequest):
    res = chat.run(question.question)
    result = copy.deepcopy(res)
    status = True
    return JSONResponse({'status': status, 'message': result})

@app.post('/api/newChat')
async def getNewChat(items: NeweChatData, request: Request) -> JSONResponse:
    host = request.headers.get('host')
    user_id = ls.getUserId(host)
    ls.updateTopicId(user_id, None)
    status = True 
    return JSONResponse({'status': status})

@app.post('/api/getUserIdAndTopicId')
async def getUserIdAndTopicId(items: UserIdAndTopicIdData, request: Request):
    host = request.headers.get('host')
    user_id = ls.getUserId(host)
    topic_id = ls.getTopicId(user_id)
    status = True
    return JSONResponse({'status': status, 'user_id': user_id, 'topic_id': topic_id})

@app.post('/api/singup')
async def singup(items: SingupRequestDTO, request: Request) -> JSONResponse:
    host = request.headers.get('host')
    login: str = items.login
    password: str = items.password
    teacher_student_flag: int = items.teacher_student_flag
    all_logins = db.getAllUsersLogin()
    
    if login in all_logins:
        status: bool = False
        return JSONResponse({'status': status, 'message': 'Пользователь с таким логином уже есть'})
     
    hash_password = hashPassword(password)
    db.addUser(login, hash_password, teacher_student_flag)
    status: bool = True
    # return JSONResponse({'status': status, 'message': 'Пользователь добавлен'})
    return JSONResponse({'status': status, 'message': 'http://127.0.0.1:5500/front/ai-chat.html'})

@app.post('/api/login')
async def login(items: LoginRequestDTO, request: Request) -> JSONResponse:
    login: str = items.login
    password: str = items.password
    all_logins = db.getAllUsersLogin()
    if all_logins != None:
        all_logins = list(map(lambda x: x[0], all_logins))

    if login not in all_logins:
        status: bool = False
        return JSONResponse({'status': status, 'message': 'Пользователя с таким логином нет'})
    new_hash_password = hashPassword(password)
    curent_hash_password = db.getPasswordFromLogin(login)
    
    if curent_hash_password != None:
        if new_hash_password != curent_hash_password[0]: 
            status: bool = False
            return JSONResponse({'status': status, 'message': 'Пароль не верный'})
        print(request.headers)
        login_id = db.getUser(login)[0]
        host = request.headers.get('host')
        ls.updateUserId(host, login_id)
        status: bool = True
        return JSONResponse({'status': status, 'message': 'http://127.0.0.1:5500/front/ai-chat.html', 'login': login_id})
    status: bool = False
    return JSONResponse({'status': status, 'message': 'Что-то пошло не так'})

@app.post('/api/addMessage')
async def addMessage(items: MessagesDataBase, request: Request) -> JSONResponse:
    topic_id = items.topic_id
    content = items.content
    is_ai = items.is_ai
    host = request.headers.get('host')
    user_id = ls.getUserId(host)
    ls.updateTopicId(user_id, topic_id)
    print(topic_id, content, is_ai)
    db.addMessage(topic_id, user_id, content, is_ai)
    status: bool = True
    return JSONResponse({'status': status, 'message': 'Сообщение добавлено'})

@app.post('/api/getMessage')
async def getMessage(items: GetMessagesDataBase, request: Request) -> JSONResponse:
    topic_id: int = items.topic_id
    user_id: int = items.user_id
    print(topic_id, user_id)
    messages = db.getMessagesFromTopicIdAndUserId(topic_id, user_id)
    status: bool = True
    return JSONResponse({'status': status, 'messages': messages})

@app.post('/api/addTopic')
async def addTopic(items: TopicsDataBase, request: Request) -> JSONResponse:
    user_id = items.user_id
    title = items.title
    date = datetime.now().strftime('%d.%m.%Y %H:%M')
    row = db.addTopic(user_id, title, date)
    topic_id = row[0]
    host = request.headers.get('host')
    user_id = ls.getUserId(host)
    ls.updateTopicId(user_id, topic_id)
    print('topic_id', row[0])
    status: bool = True
    return JSONResponse({'status': status, 'topic_id': row[0], 'message': 'Тема добавлена'})

@app.post('/api/getTopics')
async def getTopics(items: GetTopicsDataBase, request: Request) -> JSONResponse:
    login_id = items.login_id
    with sqlite3.connect('api/db.sqlite3') as c:
        topics = c.execute(f"""SELECT * FROM topics WHERE user_id = '{login_id}'""").fetchall()
    # print(topics)
    status: bool = True
    return JSONResponse({'status': status, 'topics': topics})

@app.post('/api/delTopic')
async def getTopics(items: DelTopicDataBase, request: Request) -> JSONResponse:
    topic_id = items.topic_id
    with sqlite3.connect('api/db.sqlite3') as c:
        c.execute(f"""DELETE FROM messages WHERE topic_id = '{topic_id}'""")
        c.commit()
        c.execute(f"""DELETE FROM topics WHERE id = '{topic_id}'""")
        c.commit()
    # print(topics)
    status: bool = True
    return JSONResponse({'status': status})


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}

# @app.post("/items/")
# def create_item(item: dict):
#     return item
