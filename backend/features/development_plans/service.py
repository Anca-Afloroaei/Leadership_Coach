import logging
from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from entities.development_plans import DevelopmentPlan
from .models import DevelopmentPlanCreate, DevelopmentPlanRead
from entities.users import User

logger = logging.getLogger(__name__)

# def create_assessment(assessment: DevelopmentPlanCreate, session: Session, current_user: User) -> DevelopmentPlanRead:
def create_development_plan(development_plan: DevelopmentPlanCreate, session: Session) -> DevelopmentPlanRead:
    """
    Create a new Development Plan in the database.
    """
    new_development_plan = DevelopmentPlan(
        user_id=development_plan.user_id,
        goal=development_plan.goal,
        description=development_plan.description,
        start_date=development_plan.start_date,
        end_date=development_plan.end_date,
        status=development_plan.status,
        progress=development_plan.progress,
        resources=development_plan.resources,
        challenges=development_plan.challenges,
        next_steps=development_plan.next_steps,
        action_items=development_plan.action_items,
        target_date=development_plan.target_date
    )
    session.add(new_development_plan)
    session.commit()
    session.refresh(new_development_plan)
    logger.info(f"Develpment Plan: {new_development_plan.id}")
    return new_development_plan


def get_development_plan_by_id(development_plan_id: str, session: Session) -> DevelopmentPlanRead:
    """
    Retrieve a Development Plan by its ID.
    """
    statement = select(DevelopmentPlan).where(DevelopmentPlan.id == development_plan_id)
    development_plan = session.exec(statement).first()
    if not development_plan:
        logger.error(f"Development Plan with ID {development_plan_id} not found")
        raise HTTPException(status_code=404, detail="Development Plan not found")
    logger.info(f"Development Plan retrieved: {development_plan.id}")
    return DevelopmentPlanRead.model_validate(development_plan)  # Assuming DevelopmentPlanRead has a model_validate method to convert the model 


def delete_development_plan(development_plan_id: str, session: Session) -> None:
    """
    Delete a Development Plan by its ID.
    """
    statement = select(DevelopmentPlan).where(DevelopmentPlan.id == development_plan_id)
    development_plan = session.exec(statement).first()
    if not development_plan:
        logger.error(f"Development Plan with ID {development_plan_id} not found")
        raise HTTPException(status_code=404, detail="Development Plan not found")
    session.delete(development_plan)
    session.commit()
    logger.info(f"Development Plan with ID {development_plan_id} deleted successfully")
    return None



