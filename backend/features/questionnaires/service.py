import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from entities.questionnaires import Questionnaire

from .models import QuestionnaireCreate, QuestionnaireRead, QuestionnaireUpdate

logger = logging.getLogger(__name__)


def create_questionnaire(question: QuestionnaireCreate, session: Session) -> QuestionnaireRead:
    """
    Create a new questionnaire in the system.
    """
    new_questionnaire = Questionnaire(
        title=question.title,
        description=question.description,
        questions=question.questions,
        is_active=question.is_active
    )
    session.add(new_questionnaire)
    session.commit()
    session.refresh(new_questionnaire)
    logger.info(f"Questionnaire created: {new_questionnaire.id}")
    return QuestionnaireRead.model_validate(new_questionnaire)


def get_questionnaire_by_id(questionnaire_id: str, session: Session) -> QuestionnaireRead:
    """
    Retrieve a questionnaire by its ID.
    """
    statement = select(Questionnaire).where(Questionnaire.id == questionnaire_id)
    questionnaire = session.exec(statement).first()
    if not questionnaire:
        logger.error(f"Questionnaire with ID {questionnaire_id} not found")
        raise HTTPException(status_code=404, detail="Questionnaire not found")
    logger.info(f"Questionnaire retrieved: {questionnaire.id}")
    return QuestionnaireRead.model_validate(questionnaire)


def update_questionnaire(questionnaire_update: QuestionnaireUpdate, questionnaire_id: str, session: Session) -> QuestionnaireRead:
    """
    Update an existing questionnaire's information.
    """
    statement = select(Questionnaire).where(Questionnaire.id == questionnaire_id)
    questionnaire = session.exec(statement).first()
    if not questionnaire:
        logger.error(f"Questionnaire with ID {questionnaire_id} not found")
        raise HTTPException(status_code=404, detail="Questionnaire not found")

    for key, value in questionnaire_update.model_dump().items():
        setattr(questionnaire, key, value)

    session.add(questionnaire)
    session.commit()
    session.refresh(questionnaire)
    logger.info(f"Questionnaire updated: {questionnaire.id}")
    return QuestionnaireRead.model_validate(questionnaire)


def delete_questionnaire(questionnaire_id: str, session: Session):
    """
    Delete a questionnaire by its ID.
    """
    statement = select(Questionnaire).where(Questionnaire.id == questionnaire_id)
    questionnaire = session.exec(statement).first()
    if not questionnaire:
        logger.error(f"Questionnaire with ID {questionnaire_id} not found")
        raise HTTPException(status_code=404, detail="Questionnaire not found")

    session.delete(questionnaire)
    session.commit()
    logger.info(f"Questionnaire deleted: {questionnaire.id}")
    return {"detail": "Questionnaire deleted successfully"}


def list_questionnaires(session: Session) -> list[QuestionnaireRead]:
    """
    List all questionnaires in the system.
    """
    statement = select(Questionnaire)
    questionnaires = session.exec(statement).all()
    if not questionnaires:
        logger.info("No questionnaires found")
        return []
    
    logger.info(f"Retrieved {len(questionnaires)} questionnaires")
    return [QuestionnaireRead.model_validate(questionnaire) for questionnaire in questionnaires]






