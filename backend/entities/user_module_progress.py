from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlmodel import Field, SQLModel


class UserModuleProgress(SQLModel, table=True):
    """
    User Module Progress model representing a user's progress in a module.
    This model is used to store user progress information in the database.
    """

    __tablename__ = "user_module_progress"
    id: str = Field(default_factory=lambda: uuid4().hex, primary_key=True, index=True)
    user_id: str = Field(sa_column=Column(String, ForeignKey("users.id"), nullable=False))
    module_id: str = Field(sa_column=Column(String, ForeignKey("leadership_modules.id"), nullable=False))
    status: str = Field(sa_column=Column(String, nullable=False))  # e.g: "In Progress", "Completed", "On Hold"
    progress_percentage: int = Field(sa_column=Column(Integer, nullable=False))  # Progress percentage (0-100)
    last_accessed: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False),
    )
    notes: Optional[str] = Field(sa_column=Column(String, nullable=True))  # Optional notes or comments about the module
    completed: bool = Field(default=False, sa_column=Column(Integer, nullable=False))  # Whether the module is completed
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False),
    )
    completed_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=None, nullable=True),
    )  # Optional completion date if the module is completed
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False),
    )  # Last updated timestamp