import logging
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from database.core import get_session
from entities.users import User
from entities.development_plans import DevelopmentPlan
from .models import DevelopmentPlanCreate, DevelopmentPlanRead
from .service import (
    create_development_plan as service_create_development_plan,
    get_development_plan_by_id as service_get_development_plan_by_id,
    delete_development_plan as service_delete_development_plan
)


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/devplans", tags=["development_plans"])

@router.post("/", response_model=DevelopmentPlanRead, summary="Create Development Plan")
# def create_development_plan(development_plan: DevelopmentPlanCreate, session: Session = Depends(get_session), current_user: User=Depends(get_current_user)) -> DevelopmentPlanRead:
def create_development_plan(development_plan: DevelopmentPlanCreate, session: Session = Depends(get_session)) -> DevelopmentPlanRead:

    """
    Create a new Developmemt Plan in the system.
    """
    return service_create_development_plan(development_plan, session)


# @router.get("/{development_plan_id}", response_model=DevelopmentPlanRead, summary="Get Development Plan by ID")
def get_development_plan(development_plan_id: str, session: Session = Depends(get_session)) -> DevelopmentPlanRead:
    """
    Retrieve a Development Plan by its ID.
    """
    return service_get_development_plan_by_id(development_plan_id, session) 


def delete_development_plan(development_plan_id: str, session: Session = Depends(get_session)):
    """
    Delete a Development Plan by its ID.
    """
    return service_delete_development_plan(development_plan_id, session)
