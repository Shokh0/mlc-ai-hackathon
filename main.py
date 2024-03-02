from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from services import Services
from schemes import *

import uvicorn


"""This module includes main method for working with AI assistant model."""


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

app.mount("/static", StaticFiles(directory="front/static"), name="static")
templates = Jinja2Templates(directory="front/template")
services = Services()


# Application
# GET
@app.get("/", response_class=HTMLResponse)
def indext(request: Request) -> JSONResponse:
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login(request: Request) -> JSONResponse:
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/edu-chat", response_class=HTMLResponse)
def aiChat(request: Request) -> JSONResponse:
    return templates.TemplateResponse("chat.html", {"request": request})

# Api
# GET
@app.get('/api/d')
async def readDocsApi() -> RedirectResponse: 
    return RedirectResponse(f"/docs")

@app.get('/api/r')
async def readRedocApi() -> RedirectResponse: 
    return RedirectResponse(f"/redoc")

# POST
@app.post('/api/lamini')
async def lamini(question : LaminiRequestDTO):
    return services.get_lamini(question)

@app.post('/api/newChat')
async def getNewChat(items: NewChatDataRequestDTO, request: Request) -> JSONResponse:
    return services.get_new_chat(items, request)

@app.post('/api/getUserIdAndTopicId')
async def getUserIdAndTopicId(items: UserIdAndTopicIdDataRequestDTO, request: Request):
    return services.get_user_id_and_topic_id(items, request)

@app.post('/api/singup')
async def singup(items: SingupRequestDTO, request: Request) -> JSONResponse:
    return services.get_singup(items, request)

@app.post('/api/login')
async def login(items: LoginRequestDTO, request: Request) -> JSONResponse:
    return services.get_login(items, request)

@app.post('/api/addMessage')
async def addMessage(items: AddMessagesRequestDTO, request: Request) -> JSONResponse:
    return services.add_new_message(items, request)

@app.post('/api/getMessage')
async def getMessage(items: GetMessagesRequestDTO, request: Request) -> JSONResponse:
    return services.get_messages(items, request)

@app.post('/api/addTopic')
async def addTopic(items: AddTopicRequestDTO, request: Request) -> JSONResponse:
    return services.add_topic(items, request)

@app.post('/api/getTopics')
async def getTopics(items: GetTopicsRequestDTO, request: Request) -> JSONResponse:
    return services.get_topics(items, request)

@app.post('/api/delTopic')
async def delTopic(items: DelTopicRequestDTO, request: Request) -> JSONResponse:
    return services.del_topic(items, request)


if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=80, reload=True)