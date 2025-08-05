import logging
from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from entities.user_module_progress import UserModuleProgress
from .models import UserModuleProgressCreate, UserModuleProgressRead
from entities.users import User


logger = logging.getLogger(__name__)


# def create_user_module_progress(module: UserModuleProgressCreate, session: Session, current_user: User) -> UserModuleProgressRead:
def create_user_module_progress(progress: UserModuleProgressCreate, session: Session) -> UserModuleProgressRead:
    """
    Create a new user module progress record in the system.
    """
    new_progress = UserModuleProgress(
        # user_id=progress.current_user.id,
        user_id=progress.user_id,
        module_id=progress.module_id,
        progress_percentage=progress.progress_percentage,
        status=progress.status,
        last_updated=progress.last_updated,
        notes=progress.notes
    )

    session.add(new_progress)
    session.commit()
    session.refresh(new_progress)
    logger.info(f"User Module Progress created: {new_progress.id}")
    return new_progress


def get_user_module_progress_by_id(progress_id: str, session: Session) -> UserModuleProgressRead:
    """
    Retrieve a user module progress record by its ID.
    """
    statement = select(UserModuleProgress).where(UserModuleProgress.id == progress_id)
    progress = session.exec(statement).first()
    if not progress:
        logger.error(f"User Module Progress with ID {progress_id} not found")
        raise HTTPException(status_code=404, detail="User Module Progress not found")
    logger.info(f"User Module Progress retrieved: {progress.id}")
    return UserModuleProgressRead.model_validate(progress)  # Assuming UserModuleProgressRead has a model_validate method to convert the model


def delete_user_module_progress(progress_id: str, session: Session) -> None:
    """
    Delete a user module progress record by its ID.
    """
    statement = select(UserModuleProgress).where(UserModuleProgress.id == progress_id)
    progress = session.exec(statement).first()
    if not progress:
        logger.error(f"User Module Progress with ID {progress_id} not found")
        raise HTTPException(status_code=404, detail="User Module Progress not found")
    session.delete(progress)
    session.commit()
    logger.info(f"User Module Progress with ID {progress_id} deleted successfully")
    return None



