from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from datetime import datetime



class Role(str, Enum):
    EXECUTIVE = "executive"
    MANAGER = "manager"
    ENTREPRENEUR = "entrepreneur"
    COACH = "coach"


class UserCreate(BaseModel):
    first_name: str 
    last_name: str 
    email: str 
    hashed_password: str 
    role: Role 
    industry: str 
    years_experience: int 


class UserRead(BaseModel):
    id: str
    first_name: str 
    last_name: str 
    email: EmailStr 
    role: Role 
    industry: str
    years_experience: int 
    created_at: datetime
    updated_at: datetime 

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Role] = None
    industry: Optional[str] = None
    years_experience: Optional[int] = None


