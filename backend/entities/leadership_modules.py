from uuid import uuid4
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timezone


class LeadershipModule(SQLModel, table=True):
    """
    Leadership Module model representing a module in the system.
    This model is used to store leadership module information in the database.
    """

    __tablename__ = "leadership_modules"
    id: str = Field(default_factory=lambda: uuid4().hex, primary_key=True, index=True)
    title: str = Field(sa_column=Column(String, nullable=False))
    topic: str = Field(sa_column=Column(String, nullable=False))
    format: str = Field(sa_column=Column(String, nullable=False))  # e.g: "Video", "Article", "Podcast"
    duration: int = Field(sa_column=Column(Integer, nullable=False))  # Duration in minutes
    difficulty_level: str = Field(sa_column=Column(String, nullable=False))  # e.g: "Beginner", "Intermediate", "Advanced" 
    estimated_completion_time: int = Field(
        sa_column=Column(Integer, nullable=False)
    )  # Estimated time to complete the module in minutes

    
    prerequisites: str = Field(sa_column=Column(String, nullable=True))  # Optional prerequisites
    learning_outcomes: str = Field(sa_column=Column(String, nullable=False))  # Expected outcomes after completing the module
    target_audience: str = Field(sa_column=Column(String, nullable=False))  # Who the module is intended for    



    content: str = Field(sa_column=Column(String, nullable=False))  # Content of the module
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False),
    )
    description: str = Field(sa_column=Column(String, nullable=False))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False),
    )