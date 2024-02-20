from pydantic import BaseModel
import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str


class UserUpdate(BaseModel):
    username: str
    password: str


class ImageUpdate(BaseModel):
    image_desc: str


class VoteCreate(BaseModel):
    image1: str
    image2: str
    score1: int
    score2: int


class Token(BaseModel):
    access_token: str
    token_type: str



class User(BaseModel):
    id:str
    username: str
    email: str
    role: str
    created_at: datetime.datetime


