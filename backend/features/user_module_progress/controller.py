import logging

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from database.core import get_session
from entities.user_module_progress import UserModuleProgress
from entities.users import User

from .models import UserModuleProgressCreate, UserModuleProgressRead
from .service import (
    create_user_module_progress as service_create_user_module_progress,
    delete_user_module_progress as service_delete_user_module_progress,
    get_user_module_progress_by_id as service_get_user_module_progress_by_id,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/module_progress", tags=["module_progress"])


@router.post("/", response_model=UserModuleProgressRead, summary="Create User Module Progress")
# def create_module_progress(module: LeadershipModuleProgressCreate, session: Session = Depends(get_session), current_user: User=Depends(get_current_user)) -> LeadershipModuleProgressRead:

def create_user_module_progress(
    progress: UserModuleProgressCreate, session: Session = Depends(get_session)
) -> UserModuleProgressRead:
    """
    Create a new user module progress record in the system.
    """
    return service_create_user_module_progress(progress, session)   


@router.get("/{progress_id}", response_model=UserModuleProgressRead, summary="Get User Module Progress by ID")
def get_user_module_progress(
    progress_id: str, session: Session = Depends(get_session)
) -> UserModuleProgressRead:
    """
    Retrieve a user module progress record by its ID.
    """
    return service_get_user_module_progress_by_id(progress_id, session)


@router.delete("/{progress_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete User Module Progress")
def delete_user_module_progress(progress_id: str, session: Session = Depends(get_session)):
    """
    Delete a user module progress record by its ID.
    """
    return service_delete_user_module_progress(progress_id, session)



