from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: EmailStr
    password: str
    phone: Optional[str] = None
    name: Optional[str] = None
    city: Optional[str] = None

class UserOut(BaseModel):
    id: int
    username: EmailStr
    phone: Optional[str]
    name: Optional[str]
    city: Optional[str]

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    phone: Optional[str] = None
    name: Optional[str] = None
    city: Optional[str] = None


class Token(BaseModel):
    access_token: str


class ListingCreate(BaseModel):
    type: str
    price: int
    address: str
    area: Optional[float] = None
    rooms_count: Optional[int] = None
    description: Optional[str] = None

class ListingOut(BaseModel):
    id: int
    type: str
    price: int
    address: str
    area: Optional[float]
    rooms_count: Optional[int]
    description: Optional[str]
    user_id: int
    total_comments: int = 0  

    class Config:
        orm_mode = True

class ListingUpdate(BaseModel):
    type: Optional[str] = None
    price: Optional[int] = None
    address: Optional[str] = None
    area: Optional[float] = None
    rooms_count: Optional[int] = None
    description: Optional[str] = None


class CommentCreate(BaseModel):
    content: str

class CommentOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    author_id: int

    class Config:
        orm_mode = True
