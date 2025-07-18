import logging
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from database.core import get_session
from entities.users import User
from .models import UserCreate, UserRead, UserUpdate
from .service import (
    create_user as service_create_user,
    get_user_by_id as service_get_user_by_id,
    update_user as service_update_user,
    delete_user as service_delete_user
)


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, summary="Create User")
def create_user(user: UserCreate, session: Session = Depends(get_session)) -> UserRead:
    """
    Create a new user in the system.
    """
    return service_create_user(user, session)


@router.get("/{user_id}", response_model=UserRead, summary="Get User by ID")
def get_user(user_id: str, session: Session = Depends(get_session)) -> UserRead:
    """
    Retrieve a user by their ID.
    """
    return service_get_user_by_id(user_id, session)


@router.patch("/{user_id}", response_model=UserRead, summary="Update User")
def update_user(
    user_id: str, user_update: UserUpdate, session: Session = Depends(get_session)
) -> UserRead:
    """
    Update an existing user's information.
    """
    return service_update_user(user_id, user_update, session)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete User")
def delete_user(user_id: str, session: Session = Depends(get_session)):
    """
    Delete a user by their ID.
    """
    return service_delete_user(user_id, session)