import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from entities.questions import Question

from .models import QuestionCreate, QuestionRead, QuestionUpdate

logger = logging.getLogger(__name__)


def create_question(question: QuestionCreate, session: Session) -> QuestionRead:
    """
    Create a new question in the system.
    """
    new_question = Question(
        text=question.text,
        competency=question.competency,
        explanation=question.explanation
    )
    session.add(new_question)
    session.commit()
    session.refresh(new_question)
    logger.info(f"Question created: {new_question.id}")
    return QuestionRead.model_validate(new_question)


def get_question_by_id(question_id: str, session: Session) -> QuestionRead:
    """
    Retrieve a question by its ID.
    """
    statement = select(Question).where(Question.id == question_id)
    question = session.exec(statement).first()
    if not question:
        logger.error(f"Question with ID {question_id} not found")
        raise HTTPException(status_code=404, detail="Question not found")
    logger.info(f"Question retrieved: {question.id}")
    return QuestionRead.model_validate(question)


def update_question(question_update: QuestionUpdate, question_id: str, session: Session) -> QuestionRead:
    """
    Update an existing question's information.
    """
    statement = select(Question).where(Question.id == question_id)
    question = session.exec(statement).first()
    if not question:
        logger.error(f"Question with ID {question_id} not found")
        raise HTTPException(status_code=404, detail="Question not found")

    for key, value in question_update.model_dump().items():
        setattr(question, key, value)

    session.add(question)
    session.commit()
    session.refresh(question)
    logger.info(f"Question updated: {question.id}")
    return QuestionRead.model_validate(question)


def delete_question(question_id: str, session: Session):
    """
    Delete a question by its ID.
    """
    statement = select(Question).where(Question.id == question_id)
    question = session.exec(statement).first()
    if not question:
        logger.error(f"Question with ID {question_id} not found")
        raise HTTPException(status_code=404, detail="Question not found")

    session.delete(question)
    session.commit()
    logger.info(f"Question deleted: {question.id}")
    return {"detail": "Question deleted successfully"}


def list_questions(session: Session) -> list[QuestionRead]:
    """
    List all questions in the system.
    """
    statement = select(Question)
    questions = session.exec(statement).all()
    if not questions:
        logger.info("No questions found")
        return []
    
    logger.info(f"Retrieved {len(questions)} questions")
    return [QuestionRead.model_validate(question) for question in questions]




