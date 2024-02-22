from pydantic import BaseModel, EmailStr, conint
import datetime
from enum import Enum
from typing import Optional


# role possible values
class RoleEnum(str, Enum):
    admin = "admin"
    user = "uploader"
    moderator = "voter"


# user create  model
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: RoleEnum


# user update model
class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str]=None
    fullname: Optional[str] = None
    age: Optional[int] = None


# image update model
class ImageUpdate(BaseModel):
    image_desc: Optional[str]


# vote create model
class VoteCreate(BaseModel):
    image1: str
    image2: str
    score1: int
    score2: int


class Token(BaseModel):
    access_token: str
    token_type: str
