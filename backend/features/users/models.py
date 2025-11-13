from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class Role(str, Enum):
    EXECUTIVE = "executive"
    MANAGER = "manager"
    ENTREPRENEUR = "entrepreneur"
    COACH = "coach"


class UserCreate(BaseModel):
    first_name: str 
    last_name: str 
    email: EmailStr 
    password: str 
    role: Role 
    industry: str 
    years_experience: int 


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    first_name: str 
    last_name: str 
    email: EmailStr 
    role: Role 
    industry: str
    years_experience: int 
    created_at: datetime
    updated_at: datetime 


class UserUpdate(BaseModel):
    current_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Role] = None
    industry: Optional[str] = None
    years_experience: Optional[int] = None
    password: Optional[str] = None


class UserDelete(BaseModel):
    password: str
    

class UserLogin(BaseModel):
    password: str
    email: EmailStr
