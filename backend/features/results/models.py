from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime





class UserResultRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_answers_record_id: str
    user_id: str
    questionnaire_id: str
    results: dict[str, str]  # Mapping of question IDs to answer IDs provided by the user
    completed_at: Optional[datetime] = None  # Optional completion date if the questionnaire is completed

