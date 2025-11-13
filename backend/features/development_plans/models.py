from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class DevelopmentPlanCreate(BaseModel):
    user_id: str
    user_answers_record_id: Optional[str] = None
    goal: str
    description: Optional[str] = None  # Optional details/description of the goal
    # start_date: datetime = datetime.now()
    # end_date: datetime = datetime.now()
    start_date: datetime = Field(default_factory=_utcnow)
    end_date: datetime = Field(default_factory=_utcnow)
    status: str  # e.g: "In Progress", "Completed", "On Hold"
    progress: int = 0  # Progress percentage (0-100)
    resources: Optional[str] = None  # Optional resources
    challenges: Optional[str] = None  # Optional challenges
    next_steps: Optional[str] = None  # Optional next steps to take
    action_items: str
    target_date: datetime
    plan_markdown: str = ""


class DevelopmentPlanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    user_answers_record_id: Optional[str] = None
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
    plan_markdown: str = ""



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


# ===== AI Generation Models =====

class GeneratePlanRequest(BaseModel):
    user_id: str
    user_answers_record_id: str
    focus_areas: List[str]
    duration_days: int
    role: str
    industry: str
    years_experience: int


class Milestone(BaseModel):
    """Milestone structure required by the structured response parser."""

    model_config = ConfigDict(extra="forbid")

    title: str
    summary: Optional[str] = None
    timeframe: Optional[str] = None
    key_actions: List[str] = Field(default_factory=list)
    success_metric: Optional[str] = None


class GeneratedPlanPayload(BaseModel):
    goal: str
    description: str
    action_items: List[str]
    next_steps: List[str]
    resources: List[str]
    challenges: List[str]
    milestones: List[Milestone]
    plan_markdown: str


class GeneratePlanResponse(BaseModel):
    plan: DevelopmentPlanRead
    plan_markdown: str


class DevelopmentPlanSummaryRead(BaseModel):
    plan_id: str
    user_answers_record_id: str
    questionnaire_id: str
    questionnaire_title: str
    created_at: datetime
