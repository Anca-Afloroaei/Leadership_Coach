from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AnswerCreate(BaseModel):
    question_id: str  # ID of the question being answered
    answer_text: str  # The text of the answer
    score_value: int  # Score value for the answer


class AnswerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str  # Unique identifier for the answer
    question_id: str  # ID of the question being answered
    answer_text: str  # The text of the answer
    score_value: int  # Score value for the answer
    created_at: datetime  # Timestamp when the answer was created
    updated_at: datetime  # Timestamp when the answer was last updated


class AnswerUpdate(BaseModel):
    answer_text: Optional[str] = None  # The text of the answer
    score_value: Optional[int] = None  # Score value for the answer




