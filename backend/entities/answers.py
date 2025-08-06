from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timezone
from uuid import uuid4
from typing import Optional


class Answer(SQLModel, table=True):
    """
    Answer model representing an answer in the system.
    This model is used to store answer information in the database.
    """

    __tablename__ = "answers"
    id: str = Field(default_factory=lambda: uuid4().hex, primary_key=True, index=True)
    question_id: str = Field(sa_column=Column(String, ForeignKey("questions.id"), nullable=False))
    answer_text: str = Field(sa_column=Column(String, nullable=False))  # The text of the answer
    score_value: int = Field(sa_column=Column(Integer, nullable=False))  # Score value for the answer
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False),
    )  # Last updated timestamp