from sqlmodel import Field, SQLModel
from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime, timezone
from uuid import uuid4
from typing import Optional


class Questionnaire(SQLModel, table=True):
    """
    Questionnaire model representing a questionnaire in the system.
    This model is used to store questionnaire information in the database.
    """

    __tablename__ = "questionnaires"
    id: str = Field(default_factory=lambda: uuid4().hex, primary_key=True, index=True)
    title: str = Field(sa_column=Column(String, nullable=False))  # The title of the questionnaire
    description: Optional[str] = Field(sa_column=Column(String, nullable=True))  # Optional description of the questionnaire
    questions: list[str] = Field(
        sa_column=Column(ARRAY(String), nullable=False)
    )  # List of question IDs
    is_active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))  # Whether the questionnaire is active or not
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=datetime.now, nullable=False),
    )

