import logging

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from entities.leadership_modules import LeadershipModule
from entities.users import User

from .models import LeadershipModuleCreate, LeadershipModuleRead

logger = logging.getLogger(__name__)


# def create_module(module: LeadershipModuleCreate, session: Session, current_user: User) -> LeadershipModuleRead:
def create_module(module: LeadershipModuleCreate, session: Session) -> LeadershipModuleRead:
    """
    Create a new Leadership Module in the system.
    """
    new_module = LeadershipModule(
        # user_id=module.current_user.id,
        user_id=module.user_id,
        title=module.title,
        description=module.description,
        topic=module.topic,
        format=module.format,
        duration=module.duration,
        difficulty_level=module.difficulty_level,
        estimated_completion_time=module.estimated_completion_time,
        prerequisites=module.prerequisites,
        learning_outcomes=module.learning_outcomes,
        target_audience=module.target_audience,
        content=module.content
    )

    session.add(new_module)
    session.commit()
    session.refresh(new_module)
    logger.info(f"Leadership Module created: {new_module.id}")
    return new_module


def get_module_by_id(module_id: str, session: Session) -> LeadershipModuleRead:
    """
    Retrieve a Leadership Module by its ID.
    """
    statement = select(LeadershipModule).where(LeadershipModule.id == module_id)
    module = session.exec(statement).first()
    if not module:
        logger.error(f"Leadership Module with ID {module_id} not found")
        raise HTTPException(status_code=404, detail="Leadership Module not found")
    logger.info(f"Leadership Module retrieved: {module.id}")
    return LeadershipModuleRead.model_validate(module)  # Assuming LeadershipModuleRead has a model_validate method to convert the model 


def delete_module(module_id: str, session: Session) -> None:
    """
    Delete a Leadership Module by its ID.
    """
    statement = select(LeadershipModule).where(LeadershipModule.id == module_id)
    module = session.exec(statement).first()
    if not module:
        logger.error(f"Leadership Module with ID {module_id} not found")
        raise HTTPException(status_code=404, detail="Leadership Module not found")
    session.delete(module)
    session.commit()
    logger.info(f"Leadership Module with ID {module_id} deleted successfully")
    return None 


