from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class DevelopmentPlanCreate(BaseModel):
    user_id: str
    goal: str
    description: str = None  # Optional details/description of the goal
    start_date: datetime = datetime.now()
    end_date: datetime = datetime.now()
    status: str  # e.g: "In Progress", "Completed", "On Hold"
    progress: int = 0  # Progress percentage (0-100)
    resources: Optional[str] = None  # Optional resources
    challenges: Optional[str] = None  # Optional challenges
    next_steps: Optional[str] = None  # Optional next steps to take
    action_items: str
    target_date: datetime


class DevelopmentPlanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    goal: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    status: str
    progress: int
    resources: Optional[str] = None
    challenges: Optional[str] = None
    next_steps: Optional[str] = None
    action_items: str
    target_date: datetime
    created_at: datetime
    updated_at: datetime



class DevelopmentPlanUpdate(BaseModel):
    goal: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None
    progress: Optional[int] = None
    resources: Optional[str] = None
    challenges: Optional[str] = None
    next_steps: Optional[str] = None
    action_items: Optional[str] = None
    target_date: Optional[datetime] = None