from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime



class PostBase(BaseModel):
    title:str
    content:str
    #published: bool

class PostCreate(PostBase):
    pass

class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    #created_at: datetime

    class Config:
        orm_mode =True

class Post(PostBase):
    id: int
    #owner_id: int
    created_at: datetime
    #owner: User
    
    class Config:
        orm_mode =True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Userlogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint

