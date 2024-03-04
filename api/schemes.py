from typing import Optional
from pydantic import BaseModel, Field, condecimal
from datetime import datetime, date


class UserIdAndTopicIdDataRequestDTO(BaseModel):
    something: str = Field(..., description='something')

class UserIdAndTopicIdDataResponseDTO(BaseModel):
    status:   bool        = Field(..., description='give access or not')
    user_id:  int         = Field(..., description='user id')
    topic_id: int | None  = Field(..., description='topic id')
    login:    str         = Field(..., description='user name')
    
class NewChatDataRequestDTO(BaseModel):
    something: str = Field(..., description='something')

class NewChatDataResponseDTO(BaseModel):
    status: bool = Field(..., description='give access or not')
    
class AddTopicRequestDTO(BaseModel):
    user_id: int = Field(..., description='user id')
    title:   str = Field(..., description='title of the topic')
    
class AddTopicResponseDTO(BaseModel):
    status:   bool = Field(..., description='give access or not')
    topic_id: int  = Field(..., description='topic id')

class GetTopicsRequestDTO(BaseModel):
    login_id: int = Field(..., description='login id')

class GetTopicsResponseDTO(BaseModel):
    status: bool = Field(..., description='give access or not')
    topics: list = Field(..., description='topics data')

class DelTopicRequestDTO(BaseModel):
    topic_id: int = Field(..., description='topic id')

class DelTopicResponseDTO(BaseModel):
    status: bool = Field(..., description='give access or not')

class AddMessagesRequestDTO(BaseModel):
    topic_id: int = Field(..., description='id of the topic')
    content:  str = Field(..., description='main text message')
    is_ai:    int = Field(..., description='0 - user, 1 - ai')

class AddMessagesResponseDTO(BaseModel):
    status: bool = Field(..., description='give access or not')

class GetMessagesRequestDTO(BaseModel):
    topic_id: int = Field(..., description='id of the topic')
    user_id:  int = Field(..., description='user id')

class GetMessagesResponseDTO(BaseModel):
    status:   bool = Field(..., description='give access or not')
    messages: list = Field(..., description='Messages')
    
class LaminiRequestDTO(BaseModel):
    question: str = Field(..., description='question for lamini model')
    
class LaminiResponseDTO(BaseModel):
    status:  bool = Field(..., description='question for lamini model')
    message: str = Field(..., description='response from lamini model')
    
class LoginRequestDTO(BaseModel):
    gmail:    str = Field(..., description='user\'s email')
    password: str = Field(..., description='user\'s password without hash')

class LoginResponseDTO(BaseModel):
    status: bool = Field(..., description='give access or not')
    url:    str  = Field(..., description='url for redirect')

class SingupRequestDTO(BaseModel):
    login:                str = Field(..., description='user\'s username')
    gmail:                str = Field(..., description='user\'s email')
    password:             str = Field(..., description='user\'s password without hash')
    teacher_student_flag: int = Field(..., description='teacher or student flag')
    
class SingupResponseDTO(BaseModel):
    status: bool = Field(..., description='give access or not')
    url:    str  = Field(..., description='url for redirect')