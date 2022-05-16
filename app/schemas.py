from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Literal, Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRes(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Request schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


# Response schema
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserRes
    # From fastapi docs:
    # Paydatnics orm_mode will tell the pydantic model to read the data even it is not a dict
    # So it will try to search for id = data["id"] but also id = data.id
    # converts the sqlalchemy model to a pydantic model
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    Votes: int


class Vote(BaseModel):
    post_id: int
    is_voted: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]
