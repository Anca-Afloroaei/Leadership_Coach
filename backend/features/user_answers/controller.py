import logging
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from database.core import get_session
from entities.users import User
from entities.user_answers import UserAnswer
from .models import (
    UserAnswersRecordCreate,
    UserAnswersRecordRead,
    UserAnswersRecordUpdate,
)
from .service import (
    create_user_answers_record as service_create_user_answers_record,
    get_user_answers_by_record_id as service_get_user_answers_by_record_id,
    update_user_answers_record as service_update_user_answers_record,
    # get_user_answers_by_questionnaire as service_get_user_answers_by_questionnaire,
    # get_user_answers_by_user as service_get_user_answers_by_user,
    delete_user_answers_record as service_delete_user_answers_record,
)
from features.auth.service import get_current_user


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user_answers", tags=["user_answers"])


@router.post(
    "/",
    response_model=UserAnswersRecordRead,
    summary="Create User Answers Record",
)
def create_user_answers_record(
    answer: UserAnswersRecordCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> UserAnswersRecordRead:
    """
    Create a new user answer record in the system.
    """
    return service_create_user_answers_record(answer, current_user, session)


@router.get(
    "/{answers_record_id}",
    response_model=UserAnswersRecordRead,
    summary="Get User Answers Record by ID",
)
def get_user_answers_by_record_id(
    user_answers_record_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> UserAnswersRecordRead:
    """
    Retrieve a user answers record by its ID.
    """
    return service_get_user_answers_by_record_id(
        user_answers_record_id, current_user, session
    )


@router.patch(
    "/",
    response_model=UserAnswersRecordRead,
    summary="Update User Answers Record",
)
def update_user_answers_record(
    update_data: UserAnswersRecordUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> UserAnswersRecordRead:
    """
    Update an existing user answers record.
    """
    return service_update_user_answers_record(
        update_data, current_user, session
    )


# @router.get("/questionnaire/{questionnaire_id}", response_model=list[UserAnswersRecordRead], summary="Get User Answers by Questionnaire")
# def get_user_answers_by_questionnaire(
#     questionnaire_id: str, session: Session = Depends(get_session)
# ) -> list[UserAnswersRecordRead]:
#     """
#     Retrieve user answers records by questionnaire ID.
#     """
#     return service_get_user_answers_by_questionnaire(questionnaire_id, session)


@router.delete(
    "/{user_answers_record_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete User Answers Record",
)
def delete_user_answers_record(
    user_answers_record_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> None:
    """
    Delete a user answers record by its ID.
    """
    return service_delete_user_answers_record(
        user_answers_record_id, current_user, session
    )
