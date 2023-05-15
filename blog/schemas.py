from typing import List

from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    name: str
    email: str
    blogs: List[Blog]

    class Config:
        orm_mode = True


class BlogResponse(BaseModel):
    title: str
    body: str
    author: UserResponse

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
