import logging
from fastapi import HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from entities.users import User
from .models import UserCreate, UserRead, UserUpdate, UserDelete, UserLogin
from utils.security import get_password_hash, verify_password

logger = logging.getLogger(__name__)

# def create_user(user: UserCreate, session: Session) -> UserRead:
#     """
#     Create a new user in the system.
#     Raises:
#         HTTPException(400): If a user with the same email already exists
#     """
#     # Check if user with this email already exists
#     existing_user = session.exec(
#         select(User).where(User.email == user.email)
#     ).first()
    
#     if existing_user:
#         raise HTTPException(
#             status_code=400,
#             detail=f"User with email {user.email} already exists"
#         )

#     try:
#         user = User(
#             first_name=user.first_name,
#             last_name=user.last_name,
#             email=user.email,
#             hashed_password=get_password_hash(user.password),
#             role=user.role,
#             industry=user.industry,
#             years_experience=user.years_experience
#         )
#         session.add(user)
#         session.commit()
#         session.refresh(user)
#         logger.info(f"User created: {user}")
#         return UserRead.model_validate(user)
        
#     except IntegrityError as e:
#         session.rollback()
#         logger.error(f"Failed to create user: {e}")
#         raise HTTPException(
#             status_code=400,
#             detail="Failed to create user. The email address might already be in use."
#         ) from e


# def auth_user(login_credentials: UserLogin, session: Session) -> UserRead:
#     """
#     Retrieve a user by their login details.
#     Raises:
#         HTTPException(401): If the user is invalid
#     """
#     email = login_credentials.email
#     password = login_credentials.password
    
#     user = session.exec(select(User).where(User.email == email)).first()
    
#     if not user or not verify_password(password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invaild credentials"
#         )
#     logger.info(f"User {user.id} authenticated successfully")
#     return UserRead.model_validate(user)


def read_current_user(current_user: User) -> User:
    return current_user
    


def update_user(user_update: UserUpdate, current_user: User, session: Session) -> UserRead:
    """
    Update an existing user's information.
    Raises:
        HTTPException(404): If the user is not found
    """
    data = user_update.model_dump(exclude_unset=True)

    # 1) We need to pull out and verify `current_password`
    supplied_old_password = data.pop("current_password", None)
    
    if not verify_password(supplied_old_password, current_user.hashed_password):
        logger.warning(
            f"User {current_user.id} attempted to update profile with incorrect password"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect"
        )
    logger.info(f"User {current_user.id} verified their current password successfully")
    
    # 2) If the client sent a new `password`, hash+store it:
    if "password" in data:
        new_pw = data.pop("password")
        current_user.hashed_password = get_password_hash(new_pw)
        logger.info(f"User {current_user.id} updated their password successfully.")

    # 3) Update first_name/last_name/email if present:
    if "first_name" in data:
        current_user.first_name = data["first_name"]
        logger.info(f"User {current_user.id} updated their first name successfully.")
    if "last_name" in data:
        current_user.last_name = data["last_name"]
        logger.info(f"User {current_user.id} updated their last name successfully.")
    if "email" in data:
        current_user.email = data["email"]
        logger.info(f"User {current_user.id} updated their email successfully.")
    if "role" in data:
        current_user.role = data["role"]
        logger.info(f"User {current_user.id} updated their role successfully.")
    if "industry" in data:
        current_user.industry = data["industry"]
        logger.info(f"User {current_user.id} updated their industry successfully.")
    if "years_experience" in data:
        current_user.years_experience = data["years_experience"]
        logger.info(f"User {current_user.id} updated their years of experience successfully.")
    
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return UserRead.model_validate(current_user)


def delete_user(delete_in: UserDelete, current_user: User, session: Session) -> None:
    """
    Verify that delete_in.password matches current_user.hashed_password.
    If not, raise 401. If it matches, delete and commit.
    """
    if not verify_password(delete_in.password, current_user.hashed_password):
        logger.warning(
            f"User {current_user.id} attempted to delete account with incorrect password."
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password, cannot delete account.",
        )
    logger.info(f"User {current_user.id} is deleting their account.")
    session.delete(current_user)
    session.commit()
    # Return None; controller will return a 204 No Content automatically.
    return None