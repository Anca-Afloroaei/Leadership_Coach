import logging

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from database.core import get_session
from entities.user_answers import UserAnswer
from entities.users import User
from features.auth.service import get_current_user

from .models import (
    CompletedAnswersSummaryRead,
    UserAnswersRecordCreate,
    UserAnswersRecordRead,
    UserAnswersRecordUpdate,
)
from .service import (  # get_user_answers_by_questionnaire as service_get_user_answers_by_questionnaire,; get_user_answers_by_user as service_get_user_answers_by_user,
    create_user_answers_record as service_create_user_answers_record,
    delete_user_answers_record as service_delete_user_answers_record,
    get_latest_completed_user_answers as service_get_latest_completed_user_answers,
    get_recent_user_answers as service_get_recent_user_answers,
    get_user_answers_by_record_id as service_get_user_answers_by_record_id,
    list_completed_user_answers as service_list_completed_user_answers,
    update_user_answers_record as service_update_user_answers_record,
)

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

    The `answer` parameter should be a dictionary mapping question IDs (str) to answer IDs (str).
    """
    return service_create_user_answers_record(answer, current_user, session)


# Note: Keep parameterized routes after fixed-prefix routes to avoid conflicts


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

    Partial updates can specify a dictionary mapping question IDs to answer IDs,
    allowing updates to specific answers without overwriting the entire set.
    """
    return service_update_user_answers_record(
        update_data, current_user, session
    )


@router.get(
    "/recent/{questionnaire_id}",
    response_model=UserAnswersRecordRead,
    summary="Get recent in-progress User Answers for a questionnaire",
)
def get_recent_user_answers(
    questionnaire_id: str,
    days: int = 7,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> UserAnswersRecordRead:
    return service_get_recent_user_answers(
        questionnaire_id, days, current_user, session
    )


@router.get(
    "/latest_completed/{questionnaire_id}",
    response_model=UserAnswersRecordRead,
    summary="Get latest completed User Answers for a questionnaire",
)
def get_latest_completed_user_answers(
    questionnaire_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> UserAnswersRecordRead:
    return service_get_latest_completed_user_answers(
        questionnaire_id, current_user, session
    )

@router.get(
    "/completed",
    response_model=list[CompletedAnswersSummaryRead],
    summary="List completed User Answers (optionally filter by questionnaire)",
)
def list_completed_user_answers(
    questionnaire_id: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> list[CompletedAnswersSummaryRead]:
    return service_list_completed_user_answers(
        current_user=current_user,
        session=session,
        questionnaire_id=questionnaire_id,
        limit=limit,
        offset=offset,
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

@router.get(
    "/{user_answers_record_id}",
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
