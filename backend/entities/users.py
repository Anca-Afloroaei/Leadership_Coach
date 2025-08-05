from uuid import uuid4
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from features.users.models import Role



class User(SQLModel, table=True):
    """
    User model representing a user in the system.
    This model is used to store user information in the database.
    """
   
    
    __tablename__ = "users"
    id: str = Field(default_factory=lambda: uuid4().hex, primary_key=True, index=True)
    first_name: str = Field(sa_column=Column(String, nullable=False))
    last_name: str = Field(sa_column=Column(String, nullable=False))
    email: str = Field(sa_column=Column(String, unique=True, nullable=False))
    hashed_password: str = Field(sa_column=Column(String, nullable=False))
    role: Role = Field(sa_column=Column(String, nullable=False))
    industry: str = Field(sa_column=Column(String, nullable=True))
    years_experience: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=datetime.now, nullable=False),
    )

    def __repr__(self):
        return (f"User(id={self.id}, "
        f"first_name={self.first_name}, " 
        f"last_name={self.last_name}, " 
        f"email={self.email}, role={self.role}, "
        "hashed_password=*****, "
        f"industry={self.industry}, "
        f"years_experience={self.years_experience}, "
        f"created_at={self.created_at}, "
        f"updated_at={self.updated_at}, "
        )
    

    def __str__(self):
        return (f"User: {self.first_name} {self.last_name}, "
                f"Email: {self.email}, "
                f"Role: {self.role}, "
                f"Industry: {self.industry}, "
                f"Experience: {self.years_experience} years")
