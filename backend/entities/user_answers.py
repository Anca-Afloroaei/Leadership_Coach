from sqlmodel import Field, SQLModel
from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime, timezone
from uuid import uuid4
from typing import Optional
from entities import User, Questionnaire



class UserAnswer(SQLModel, table=True):
    """
    UserAnswer model representing user responses to questionnaires.
    This model is used to store user answers in the database.
    It includes fields for the questionnaire title, description,
    questions, active status, and timestamps for creation and updates.  
    """

    __tablename__ = "user_answers"
    id: str = Field(default_factory=lambda: uuid4().hex, primary_key=True, index=True)
    user_id: str = Field(
        sa_column=Column(ForeignKey("users.id"), nullable=False)
    )  # The ID of the user who answered the questionnaire
    questionnaire_id: str = Field(
        sa_column=Column(ForeignKey("questionnaires.id"), nullable=False)
    )  # The ID of the questionnaire being answered
    answers: list[str] = Field(
        sa_column=Column(ARRAY(String), nullable=False)
    )  # List of answers provided by the user
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False),
    )
    completed_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=None, nullable=True),
    )  # Optional completion date if the questionnaire is completed

    

