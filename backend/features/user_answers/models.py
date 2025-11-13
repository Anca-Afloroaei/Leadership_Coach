from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserAnswersRecordCreate(BaseModel):
    user_id: str
    questionnaire_id: str
    answers: dict[str, str]  # Mapping of question IDs to answer IDs provided by the user


class UserAnswersRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    questionnaire_id: str
    answers: dict[str, str]  # Mapping of question IDs to answer IDs provided by the user
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None  # Optional completion date if the questionnaire is completed


class UserAnswersRecordUpdate(BaseModel):
    id: str
    answers: Optional[dict[str, str]] = None  # Mapping of question IDs to answer IDs provided by the user
    completed_at: Optional[datetime] = None  # Optional completion date if the questionnaire is completed



class CompletedAnswersSummaryRead(BaseModel):
    """Summary view for completed results in the navbar dropdown."""
    id: str
    questionnaire_id: str
    questionnaire_title: str
    completed_at: datetime


