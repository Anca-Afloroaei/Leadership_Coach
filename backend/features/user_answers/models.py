from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime



class UserAnswerCreate(BaseModel):
    user_id: str
    questionnaire_id: str
    answers: list[str]  # List of answers provided by the user


class UserAnswerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    questionnaire_id: str
    answers: list[str]  # List of answers provided by the user
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None  # Optional completion date if the questionnaire is completed


class UserAnswerUpdate(BaseModel):
    answers: Optional[list[str]] = None  # List of answers provided by the user
    completed_at: Optional[datetime] = None  # Optional completion date if the questionnaire is completed



