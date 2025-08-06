import logging
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from database.core import get_session
from entities.users import User
from entities.user_answers import UserAnswer
from .models import UserAnswerCreate, UserAnswerRead, UserAnswerUpdate
from .service import (
    create_user_answer as service_create_user_answer,
    get_user_answers_by_record_id as service_get_user_answers_by_record_id,
    update_user_answer as service_update_user_answer,
    get_user_answers_by_questionnaire as service_get_user_answers_by_questionnaire,
    # get_user_answers_by_user as service_get_user_answers_by_user,
    delete_user_answer as service_delete_user_answer
)


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user_answers", tags=["user_answers"])


@router.post("/", response_model=UserAnswerRead, summary="Create User Answer")
def create_user_answers_record(
    answer: UserAnswerCreate, session: Session = Depends(get_session)
) -> UserAnswerRead:
    """
    Create a new user answer record in the system.
    """
    return service_create_user_answer(answer, session)


@router.get("/{answers_record_id}", response_model=UserAnswerRead, summary="Get User Answer by ID")
def get_user_answers_by_record_id(
    answers_record_id: str, session: Session = Depends(get_session)
) -> UserAnswerRead:
    """
    Retrieve a user answers record by its ID.
    """
    return service_get_user_answers_by_record_id(answers_record_id, session)


@router.patch("/", response_model=UserAnswerRead, summary="Update User Answers")
def update_user_answers_record(
    update_data: UserAnswerUpdate,
    session: Session = Depends(get_session),
) -> UserAnswerRead:
    """
    Update an existing user answers record.
    """
    return service_update_user_answer(update_data, session)


# @router.get("/questionnaire/{questionnaire_id}", response_model=list[UserAnswerRead], summary="Get User Answers by Questionnaire")
# def get_user_answers_by_questionnaire(
#     questionnaire_id: str, session: Session = Depends(get_session)
# ) -> list[UserAnswerRead]:
#     """
#     Retrieve user answers records by questionnaire ID.
#     """
#     return service_get_user_answers_by_questionnaire(questionnaire_id, session)


@router.delete("/{answers_record_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete User Answer")
def delete_user_answers_record(
    answers_record_id: str, session: Session = Depends(get_session)
) -> None:
    """
    Delete a user answers record by its ID.
    """
    return service_delete_user_answer(answers_record_id, session)






