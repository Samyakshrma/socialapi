from pydantic import BaseModel,EmailStr
from datetime import datetime


class UpdatePost(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(BaseModel):
    title: str
    content: str
    published: bool


class Post(BaseModel):
    # id: int
    title: str
    content: str
    published: bool
    # created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    # created_at: datetime

    class Config:
        orm_mode = True