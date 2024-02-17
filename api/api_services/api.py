from typing import List, Dict
from pydantic import fields
from pydantic.main import BaseModel
from pydantic.types import condecimal
from fastapi import FastAPI

from services import Services
from schemes import UsersDataBase, TopicsDataBase, MessagesDataBase, LoginRequestDTO, LoginResponseDTO

app = FastAPI()
users_database = UsersDataBase()
topics_database = TopicsDataBase()
messages_database = MessagesDataBase()

services_object = Services()

@app.post("/login", response_model=LoginResponseDTO)
async def loginSystem(request: LoginRequestDTO):
    return services_object.get_login(request.login, request.password, request.teacher_student_flag)