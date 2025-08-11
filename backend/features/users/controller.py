import logging
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from database.core import get_session
from entities.users import User
from .models import UserCreate, UserRead, UserUpdate, UserDelete, UserLogin
from .service import (
    # create_user as service_create_user,
    # auth_user as service_auth_user,
    update_user as service_update_user,
    delete_user as service_delete_user,
    read_current_user as service_read_current_user
)
from features.auth.service import get_current_user 


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])

# @router.post("/", response_model=UserRead, summary="Create User")
# def create_user(user: UserCreate, session: Session = Depends(get_session)) -> UserRead:
#     """
#     Create a new user in the system.
#     """
#     return service_create_user(user, session)


# @router.post("/user", response_model=UserRead, summary="Authenticate User")
# def auth_user(login_credentials: UserLogin, session: Session = Depends(get_session)) -> UserRead:
#     """
#     Retrieve a user by login details.
#     """
#     return service_auth_user(login_credentials, session)


@router.get("/user", response_model=UserRead, summary="Return Authenticated User")
def read_user(
    current_user: User=Depends(get_current_user)
): 
    logger.info(f"GET /users/user -user_id={current_user.id}")
    return service_read_current_user(current_user)


@router.patch("/user", response_model=UserRead, summary="Update User")
def update_user(
    user_update: UserUpdate, current_user: User=Depends(get_current_user), session: Session=Depends(get_session)
) -> UserRead:
    """
    Update an existing user's information.
    """
    return service_update_user(user_update, current_user, session)


@router.delete("/user", status_code=status.HTTP_204_NO_CONTENT, summary="Delete User")
def delete_user(delete_in: UserDelete, current_user: User=Depends(get_current_user), session: Session=Depends(get_session)):
    """
    Delete a user by their ID.
    """
    return service_delete_user(delete_in, current_user, session)