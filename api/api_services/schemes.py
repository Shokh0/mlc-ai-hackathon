from typing import Optional
from pydantic import BaseModel, Field, condecimal
from datetime import datetime, date


class UserIdAndTopicIdData(BaseModel):
    something: str = Field(..., description='something')
    
class NeweChatData(BaseModel):
    something: str = Field(..., description='something')
    

class UsersDataBase(BaseModel):
    login: str = Field(..., description='user\'s login data')
    password: str = Field(..., description='Users\' password')
    role: int = Field(..., description='user\'s role')

class TopicsDataBase(BaseModel):
    user_id: int = Field(..., description='user id')
    title: str = Field(..., description='title of the topic')
    # date: str = Field(..., description='date of the topic')

class GetTopicsDataBase(BaseModel):
    login_id: int = Field(..., description='login id')

class MessagesDataBase(BaseModel):
    topic_id: int = Field(..., description='id of the topic')
    content: str = Field(..., description='main text message')
    is_ai: int = Field(..., description='0 - user, 1 - ai')

class GetMessagesDataBase(BaseModel):
    topic_id: int = Field(..., description='id of the topic')
    user_id: int = Field(..., description='user id')
    

class LoginRequestDTO(BaseModel):
    login: str = Field(..., description='user\'s username or email')
    password: str = Field(..., description='user\'s password without hash')

class SingupRequestDTO(BaseModel):
    login: str = Field(..., description='user\'s username or email')
    password: str = Field(..., description='user\'s password without hash')
    teacher_student_flag: int = Field(..., description='teacher or student flag')

class LaminiRequest(BaseModel):
    question: str = Field(..., description='question for lamini model')
    
class LoginResponseDTO(BaseModel):
    response: bool = Field(..., description='give access or not')

class SingupResponseDTO(BaseModel):
    response: bool = Field(..., description='give access or not')