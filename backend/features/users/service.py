import logging
from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from entities.users import User
from .models import UserCreate, UserRead, UserUpdate

logger = logging.getLogger(__name__)

def create_user(user: UserCreate, session: Session) -> UserRead:
    """
    Create a new user in the system.
    Raises:
        HTTPException(400): If a user with the same email already exists
    """
    # Check if user with this email already exists
    existing_user = session.exec(
        select(User).where(User.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail=f"User with email {user.email} already exists"
        )

    try:
        db_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hashed_password=user.hashed_password,
            role=user.role,
            industry=user.industry,
            years_experience=user.years_experience
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        logger.info(f"User created: {db_user}")
        return db_user
    except IntegrityError as e:
        session.rollback()
        logger.error(f"Failed to create user: {e}")
        raise HTTPException(
            status_code=400,
            detail="Failed to create user. The email address might already be in use."
        ) from e


def get_user_by_id(user_id: str, session: Session) -> UserRead:
    """
    Retrieve a user by their ID.
    Raises:
        HTTPException(404): If the user is not found
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"User retrieved: {user}")
    return user


def update_user(user_id: str, user_update: UserUpdate, session: Session) -> UserRead:
    """
    Update an existing user's information.
    Raises:
        HTTPException(404): If the user is not found
    """
    user = get_user_by_id(user_id, session)
    
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    logger.info(f"User updated: {user}")
    
    return user


def delete_user(user_id: str, session: Session) -> None:
    """
    Delete a user by their ID.
    Raises:
        HTTPException(404): If the user is not found
    """
    user = get_user_by_id(user_id, session)
    
    session.delete(user)
    session.commit()
    logger.info(f"User deleted: {user}")
    
    return None