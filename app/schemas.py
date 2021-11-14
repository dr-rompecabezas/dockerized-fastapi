from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


# User
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Post
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    created_at: datetime
    id: int
    owner_id: int
    owner: User

    class Config:
        orm_mode = True


class PostList(PostBase):
    id: int

    class Config:
        orm_mode = True


class PostVotes(BaseModel):
    # Extend BaseModel, not PostBase
    Post: Post
    votes: int

    class Config:
        orm_mode = True


# Token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

# Vote
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
