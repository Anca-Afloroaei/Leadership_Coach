from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlmodel import Field, SQLModel


class LeadershipAssessment(SQLModel, table=True):
    """Leadership Assessment model representing a leadership assessment in the system.
    This model is used to store leadership assessment information in the database."""

    __tablename__ = "leadership_assessments"
    id: str = Field(default_factory=lambda: uuid4().hex, primary_key=True, index=True)
    user_id: str = Field(sa_column=Column(String, ForeignKey("users.id"), nullable=False))
    self_rating: int = Field(sa_column=Column(Integer, nullable=False))
    assessment_rating: int = Field(sa_column=Column(Integer, nullable=False))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False),
    )