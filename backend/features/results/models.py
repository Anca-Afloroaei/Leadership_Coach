from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserResultRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_answers_record_id: str
    user_id: str
    questionnaire_id: str
    # Mapping of competency -> percentage (0-100)
    results: dict[str, float]
    completed_at: Optional[datetime] = None  # Optional completion date if the questionnaire is completed
