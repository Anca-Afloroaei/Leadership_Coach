from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class QuestionCreate(BaseModel):
    question_text: str # The text of the question
    competency: str # Optional competency of the question
    explanation: Optional[str] = None # Optional explanation or context for the question - Make this NOT Optional LATER
    

class QuestionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str  # Unique identifier for the question
    question_text: str  # The text of the question
    competency: Optional[str] = None  # Optional competency of the question
    explanation: Optional[str] = None  # Optional explanation or context for the question
    is_active: bool  # Whether the question is active or not
    created_at: datetime  # Timestamp when the question was created
    updated_at: datetime  # Timestamp when the question was last updated


class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None  # The text of the question
    competency: Optional[str] = None  # Optional competency of the question
    explanation: Optional[str] = None  # Optional explanation or context for the question
    is_active: Optional[bool] = None  # Whether the question is active or not


