from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class QuestionnaireCreate(BaseModel):
    title: str  # Title of the questionnaire
    description: Optional[str] = None  # Optional description of the questionnaire
    questions: list[str]  # List of questions in the questionnaire
    is_active: bool = True  # Whether the questionnaire is active or not


class QuestionnaireRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str  # Unique identifier for the questionnaire
    title: str  # Title of the questionnaire
    description: Optional[str] = None  # Optional description of the questionnaire
    questions: list[str]  # List of question IDs
    is_active: bool  # Whether the questionnaire is active or not
    created_at: datetime  # Timestamp when the questionnaire was created
    updated_at: datetime  # Timestamp when the questionnaire was last updated


class QuestionnaireUpdate(BaseModel):
    title: Optional[str] = None  # Title of the questionnaire
    description: Optional[str] = None  # Optional description of the questionnaire
    questions: Optional[list[str]] = None  # List of question IDs
    is_active: Optional[bool] = None  # Whether the questionnaire is active or not


