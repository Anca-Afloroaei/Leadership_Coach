from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlmodel import Field, SQLModel


class Question(SQLModel, table=True):
    """
    Question model representing a question in the system.
    This model is used to store question information in the database.
    """

    __tablename__ = "questions"
    id: str = Field(default_factory=lambda: uuid4().hex, primary_key=True, index=True)
    question_text: str = Field(sa_column=Column(String, nullable=False))  # The text of the question
    competency: str = Field(sa_column=Column(String, nullable=True))  # Optional competency of the question
    explanation: Optional[str] = Field(
        sa_column=Column(String, nullable=True)
    )  # Optional explanation or context for the question - Make this NOT Optional LATER
    is_active: bool = Field(
        default=True, sa_column=Column(Boolean, nullable=False)
    )  # Whether the question is active or not
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False),
    )