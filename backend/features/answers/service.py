import logging
from fastapi import HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from entities.answers import Answer
from .models import AnswerCreate, AnswerRead, AnswerUpdate


logger = logging.getLogger(__name__)


def create_answer(answer: AnswerCreate, session: Session) -> AnswerRead:
    """
    Create a new answer in the system.
    """
    new_answer = Answer(
        question_id=answer.question_id,
        answer_text=answer.answer_text,
        score_value=answer.score_value
    )
    session.add(new_answer)
    session.commit()
    session.refresh(new_answer)
    logger.info(f"Answer created: {new_answer.id}")
    return AnswerRead.model_validate(new_answer)


def get_answer_by_id(answer_id: str, session: Session) -> AnswerRead:
    """
    Retrieve an answer by its ID.
    """
    statement = select(Answer).where(Answer.id == answer_id)
    answer = session.exec(statement).first()
    if not answer:
        logger.error(f"Answer with ID {answer_id} not found")
        raise HTTPException(status_code=404, detail="Answer not found")
    logger.info(f"Answer retrieved: {answer.id}")
    return AnswerRead.model_validate(answer)


def update_answer(answer_update: AnswerUpdate, answer_id: str, session: Session) -> AnswerRead:
    """
    Update an existing answer's information.
    """
    statement = select(Answer).where(Answer.id == answer_id)
    answer = session.exec(statement).first()
    
    if not answer:
        logger.error(f"Answer with ID {answer_id} not found")
        raise HTTPException(status_code=404, detail="Answer not found")
    
    for key, value in answer_update.model_dump().items():
        setattr(answer, key, value)
    
    session.add(answer)
    session.commit()
    session.refresh(answer)
    logger.info(f"Answer updated: {answer.id}")
    return AnswerRead.model_validate(answer)


def delete_answer(answer_id: str, session: Session):
    """
    Delete an answer by its ID.
    """
    statement = select(Answer).where(Answer.id == answer_id)
    answer = session.exec(statement).first()
    
    if not answer:
        logger.error(f"Answer with ID {answer_id} not found")
        raise HTTPException(status_code=404, detail="Answer not found")
    
    session.delete(answer)
    session.commit()
    logger.info(f"Answer deleted: {answer.id}")
    return {"detail": "Answer deleted successfully"}


def list_answers(question_id: str, session: Session) -> list[AnswerRead]:
    """
    List all answers for a specific question.
    """
    statement = select(Answer).where(Answer.question_id == question_id)
    answers = session.exec(statement).all()
    
    if not answers:
        logger.warning(f"No answers found for question ID {question_id}")
        return []
    
    logger.info(f"Answers retrieved for question ID {question_id}: {len(answers)}")
    return [AnswerRead.model_validate(answer) for answer in answers]


