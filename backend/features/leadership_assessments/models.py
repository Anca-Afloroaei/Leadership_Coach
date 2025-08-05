from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LeadershipAssessmentCreate(BaseModel):
    user_id: str
    self_rating: int
    assessment_rating: int


class LeadershipAssessmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str 
    user_id: str 
    self_rating: int 
    assessment_rating: int
    created_at: datetime

