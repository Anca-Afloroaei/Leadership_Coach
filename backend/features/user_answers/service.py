import logging
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from entities.questionnaires import Questionnaire
from entities.user_answers import UserAnswer
from entities.users import User

from .models import (
    CompletedAnswersSummaryRead,
    UserAnswersRecordCreate,
    UserAnswersRecordRead,
    UserAnswersRecordUpdate,
)

logger = logging.getLogger(__name__)


def create_user_answers_record(
    user_answers_record: UserAnswersRecordCreate,
    current_user: User,
    session: Session,
) -> UserAnswersRecordRead:
    """
    Create a new User Answers Record in the database.
    """
    if user_answers_record.user_id != current_user.id:
        logger.error(
            f"User Answers Record with ID {user_answers_record.user_id} does not match Current User ID"
        )
        raise HTTPException(status_code=401, detail="Unauthorized Access")
    new_record = UserAnswer(
        user_id=user_answers_record.user_id,
        questionnaire_id=user_answers_record.questionnaire_id,
        answers=user_answers_record.answers,
    )
    session.add(new_record)
    session.commit()
    session.refresh(new_record)
    logger.info(f"User Answers Record: {new_record.id}")
    return new_record


def get_user_answers_by_record_id(
    user_answers_record_id: str, current_user: User, session: Session
) -> UserAnswersRecordRead:
    """
    Retrieve a User Answers Record by its ID.
    """
    statement = select(UserAnswer).where(
        UserAnswer.id == user_answers_record_id
    )
    user_answers_record = session.exec(statement).first()
    if not user_answers_record:
        logger.error(
            f"User Answers Record with ID {user_answers_record_id} not found"
        )
        raise HTTPException(
            status_code=404, detail="User Answers Record not found"
        )
    if user_answers_record.user_id != current_user.id:
        logger.error(
            f"User Answers Record with ID {user_answers_record.id} does not match Current User ID"
        )
        raise HTTPException(status_code=401, detail="Unauthorized Access")

    logger.info(f"User Answers Record retrieved: {user_answers_record.id}")
    return UserAnswersRecordRead.model_validate(
        user_answers_record
    )  # Assuming UserAnswersRecordRead has a model_validate method to convert the model


def update_user_answers_record(
    user_answer_update: UserAnswersRecordUpdate,
    current_user: User,
    session: Session,
) -> UserAnswersRecordRead:
    """
    Update an existing User Answers Record's information.

    Supports partial updates to the answers JSONB field, which is a mapping of question IDs to answer IDs.
    Merges new answers with existing ones to avoid overwriting unrelated keys.
    Rejects updates if the record is already completed (completed_at is not None).
    """
    statement = select(UserAnswer).where(
        UserAnswer.id == user_answer_update.id
    )
    user_answers_record = session.exec(statement).first()
    if not user_answers_record:
        logger.error(
            f"User Answers Record with ID {user_answer_update.id} not found"
        )
        raise HTTPException(
            status_code=404, detail="User Answers Record not found"
        )
    if user_answers_record.user_id != current_user.id:
        logger.error(
            f"User Answers Record with ID {user_answers_record.id} does not match Current User ID"
        )
        raise HTTPException(status_code=401, detail="Unauthorized Access")
    if user_answers_record.completed_at is not None:
        logger.error(
            f"User Answers Record with ID {user_answers_record.id} is already completed and cannot be updated"
        )
        raise HTTPException(
            status_code=400, detail="Cannot update a completed User Answers Record"
        )

    update_data = user_answer_update.model_dump(exclude_unset=True)
    if "answers" in update_data and update_data["answers"] is not None:
        existing_answers = user_answers_record.answers or {}
        # Merge existing answers with new answers
        merged_answers = {**existing_answers, **update_data["answers"]}
        user_answers_record.answers = merged_answers
        update_data.pop("answers")

    for key, value in update_data.items():
        setattr(user_answers_record, key, value)

    # session.add(user_answers_record)
    session.commit()
    session.refresh(user_answers_record)
    logger.info(f"User Answers Record updated: {user_answers_record.id}")
    return UserAnswersRecordRead.model_validate(user_answers_record)


def delete_user_answers_record(
    user_answers_record_id: str, current_user: User, session: Session
) -> None:
    """
    Delete a User Answers Record by its ID.
    """
    statement = select(UserAnswer).where(
        UserAnswer.id == user_answers_record_id
    )
    user_answers_record = session.exec(statement).first()
    if not user_answers_record:
        logger.error(
            f"User Answers Record with ID {user_answers_record_id} not found"
        )
        raise HTTPException(
            status_code=404, detail="User Answers Record not found"
        )
    if user_answers_record.user_id != current_user.id:
        logger.error(
            f"User Answers Record with ID {user_answers_record.id} does not match Current User ID"
        )
        raise HTTPException(status_code=401, detail="Unauthorized Access")
    session.delete(user_answers_record)
    session.commit()
    logger.info(
        f"User Answers Record with ID {user_answers_record_id} deleted successfully"
    )
    return None


def get_recent_user_answers(
    questionnaire_id: str,
    days: int,
    current_user: User,
    session: Session,
) -> UserAnswersRecordRead:
    """
    Fetch the most recent User Answers Record for the given questionnaire within the last `days` days.
    Returns 404 if none exist within the window.
    """
    window_start = datetime.now(timezone.utc) - timedelta(days=days)
    stmt = (
        select(UserAnswer)
        .where(
            (UserAnswer.user_id == current_user.id)
            & (UserAnswer.questionnaire_id == questionnaire_id)
            & (UserAnswer.created_at >= window_start)
        )
        .order_by(UserAnswer.created_at.desc())
    )
    record = session.exec(stmt).first()
    if not record:
        raise HTTPException(status_code=404, detail="No recent user answers found")
    return UserAnswersRecordRead.model_validate(record)


def get_latest_completed_user_answers(
    questionnaire_id: str,
    current_user: User,
    session: Session,
) -> UserAnswersRecordRead:
    """
    Fetch the latest completed (completed_at is not null) User Answers Record
    for the current user and given questionnaire. Returns 404 if none exist.
    """
    stmt = (
        select(UserAnswer)
        .where(
            (UserAnswer.user_id == current_user.id)
            & (UserAnswer.questionnaire_id == questionnaire_id)
            & (UserAnswer.completed_at.isnot(None))
        )
        .order_by(UserAnswer.completed_at.desc())
    )
    record = session.exec(stmt).first()
    if not record:
        raise HTTPException(status_code=404, detail="No completed user answers found")
    return UserAnswersRecordRead.model_validate(record)


def list_completed_user_answers(
    current_user: User,
    session: Session,
    questionnaire_id: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> list[CompletedAnswersSummaryRead]:
    """Return all completed user answers for the current user, newest first.

    Optionally filter by questionnaire_id and apply limit/offset for pagination.
    """
    stmt = (
        select(UserAnswer, Questionnaire)
        .join(Questionnaire, Questionnaire.id == UserAnswer.questionnaire_id)
        .where(
            (UserAnswer.user_id == current_user.id)
            & (UserAnswer.completed_at.isnot(None))
        )
        .order_by(UserAnswer.completed_at.desc())
    )
    if questionnaire_id:
        stmt = stmt.where(UserAnswer.questionnaire_id == questionnaire_id)
    if offset:
        stmt = stmt.offset(offset)
    if limit:
        stmt = stmt.limit(limit)

    rows = session.exec(stmt).all()
    results: list[CompletedAnswersSummaryRead] = []
    for ua, q in rows:
        # Safeguard if title missing
        title = getattr(q, 'title', '') or q.id
        if ua.completed_at is None:
            # Should not happen due to filter, but guard anyway
            continue
        results.append(
            CompletedAnswersSummaryRead(
                id=ua.id,
                questionnaire_id=ua.questionnaire_id,
                questionnaire_title=title,
                completed_at=ua.completed_at,
            )
        )
    return results
