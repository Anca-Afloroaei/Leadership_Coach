import logging

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from database.core import get_session
from entities.user_answers import UserAnswer
from entities.users import User
from features.auth.service import get_current_user

from .models import UserResultRead
from .service import (
    get_user_results_by_record_id as service_get_user_results_by_record_id,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/results", tags=["results"])

@router.get(
    "/{user_answers_record_id}",
    response_model=UserResultRead,
    summary="Get computed results by user answers record ID",
)
def get_user_results_by_record_id(
    user_answers_record_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> UserResultRead:
    """
    Retrieve a user answers record by its ID.
    """
    return service_get_user_results_by_record_id(
        user_answers_record_id, current_user, session
    )
