from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime



class UserAnswersRecordCreate(BaseModel):
    user_id: str
    questionnaire_id: str
    answers: list[str]  # List of answers provided by the user


class UserAnswersRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    questionnaire_id: str
    answers: list[str]  # List of answers provided by the user
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None  # Optional completion date if the questionnaire is completed


class UserAnswersRecordUpdate(BaseModel):
    id: str
    answers: Optional[list[str]] = None  # List of answers provided by the user
    completed_at: Optional[datetime] = None  # Optional completion date if the questionnaire is completed



