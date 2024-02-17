from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel
from typing import Union
from starlette.responses import JSONResponse
from api.api_services.schemes import *
from api.database_handler import *
from api.utils.usefull_func import hashPassword

app = FastAPI()
db = DataBase()

@app.get("/")
def read_root() -> JSONResponse:
    return JSONResponse({"message": "Hello, World"})

@app.get('/d')
async def readDocsApi() -> RedirectResponse: 
    return RedirectResponse(f"/docs")

@app.get('/r')
async def readRedocApi() -> RedirectResponse: 
    return RedirectResponse(f"/redoc")

@app.post('/api/singup')
async def singupApi(items: SingupRequestDTO) -> JSONResponse:
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
    return JSONResponse({'status': status, 'message': 'Пользователь добавлен'})

@app.post('/api/login')
async def loginApi(items: LoginRequestDTO) -> JSONResponse:
    login: str = items.login
    password: str = items.password
    all_logins = db.getAllUsersLogin()
    if login in all_logins:
        status: bool = False
        return JSONResponse({'status': status, 'message': 'Пользователя с таким логином нет'})
    new_hash_password = hashPassword(password)
    curent_hash_password = db.getPasswordFromLogin(login)
    if new_hash_password != curent_hash_password: 
        status: bool = False
        return JSONResponse({'status': status, 'message': 'Пароль не верный'})
    
    status: bool = True
    return JSONResponse({'status': status, 'message': 'Верификация пройдена'})

@app.post('/api/addMessage')
async def addMessageApi(items: MessagesDataBase) -> JSONResponse:
    topic_id = items.topic_id
    content = items.content
    db.addMessage(topic_id, content)
    status: bool = True
    return JSONResponse({'status': status, 'message': 'Сообщение добавлено'})

@app.post('/api/addTopic')
async def addTopicApi(items: TopicsDataBase) -> JSONResponse:
    user_id = items.user_id
    title = items.title
    date = datetime.now().strftime('%d.%m.%Y %H:%M')
    db.addTopic(user_id, title, date)
    status: bool = True
    return JSONResponse({'status': status, 'message': 'Тема добавлена'})


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}

# @app.post("/items/")
# def create_item(item: dict):
#     return item
