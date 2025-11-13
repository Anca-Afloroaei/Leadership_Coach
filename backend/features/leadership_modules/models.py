from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LeadershipModuleCreate(BaseModel):
    title: str
    description: Optional[str] = None  # Optional details/description of the module
    topic: str
    format: str  # e.g: "Video", "Article", "Podcast"
    duration: int  # Duration in minutes
    difficulty_level: str  # e.g: "Beginner", "Intermediate", "Advanced"
    estimated_completion_time: int  # Estimated time to complete the module in minutes
    prerequisites: Optional[str] = None  # Optional prerequisites
    learning_outcomes: str  # Expected outcomes after completing the module
    target_audience: str  # Who the module is intended for
    content: str  # Content of the module


class LeadershipModuleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    description: Optional[str] = None
    topic: str
    format: str  # e.g: "Video", "Article", "Podcast"
    duration: int  # Duration in minutes
    difficulty_level: str  # e.g: "Beginner", "Intermediate", "Advanced"
    estimated_completion_time: int  # Estimated time to complete the module in minutes
    prerequisites: Optional[str] = None  # Optional prerequisites
    learning_outcomes: str  # Expected outcomes after completing the module
    target_audience: str  # Who the module is intended for
    content: str  # Content of the module
    created_at: datetime
    updated_at: datetime


class LeadershipModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    topic: Optional[str] = None
    format: Optional[str] = None  # e.g: "Video", "Article", "Podcast"
    duration: Optional[int] = None  # Duration in minutes
    difficulty_level: Optional[str] = None  # e.g: "Beginner", "Intermediate", "Advanced"
    estimated_completion_time: Optional[int] = None  # Estimated time to complete the module in minutes
    prerequisites: Optional[str] = None  # Optional prerequisites
    learning_outcomes: Optional[str] = None  # Expected outcomes after completing the module
    target_audience: Optional[str] = None  # Who the module is intended for
    content: Optional[str] = None  # Content of the module


