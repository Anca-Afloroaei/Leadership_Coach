import logging
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from database.core import get_session
from entities.users import User
from entities.leadership_modules import LeadershipModule
from .models import LeadershipModuleCreate, LeadershipModuleRead
from .service import (
    create_module as service_create_module,
    get_module_by_id as service_get_module_by_id,
    delete_module as service_delete_module
)


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/modules", tags=["modules"])

@router.post("/", response_model=LeadershipModuleRead, summary="Create Leadership Module")
# def create_module(module: LeadershipModuleCreate, session: Session = Depends(get_session), current_user: User=Depends(get_current_user)) -> LeadershipModuleRead:
def create_module(module: LeadershipModuleCreate, session: Session = Depends(get_session)) -> LeadershipModuleRead:

    """
    Create a new Leadership Module in the system.
    """
    return service_create_module(module, session)


@router.get("/{module_id}", response_model=LeadershipModuleRead, summary="Get Leadership Module by ID")
def get_module(module_id: str, session: Session = Depends(get_session)) -> LeadershipModuleRead:
    """
    Retrieve a Leadership Module by its ID.
    """
    return service_get_module_by_id(module_id, session)


@router.delete("/{module_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Leadership Module")
def delete_module(module_id: str, session: Session = Depends(get_session)):
    """
    Delete a Leadership Module by its ID.
    """
    return service_delete_module(module_id, session)

