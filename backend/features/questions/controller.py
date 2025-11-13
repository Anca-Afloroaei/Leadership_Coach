import logging

from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select

from database.core import get_session
from entities.questions import Question

from .models import QuestionCreate, QuestionRead, QuestionUpdate
from .service import (
    create_question as service_create_question,
    delete_question as service_delete_question,
    get_question_by_id as service_get_question_by_id,
    list_questions as service_list_questions,
    update_question as service_update_question,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/questions", tags=["questions"])

@router.post("/", response_model=QuestionRead, summary="Create Question")
def create_question(question: QuestionCreate, session: Session = Depends(get_session)) -> QuestionRead:
    """
    Create a new question in the system.
    """
    return service_create_question(question, session)


@router.get("/{question_id}", response_model=QuestionRead, summary="Get Question by ID")
def get_question(question_id: str, session: Session = Depends(get_session)) -> QuestionRead:
    """
    Retrieve a question by its ID.
    """
    return service_get_question_by_id(question_id, session)


@router.patch("/{question_id}", response_model=QuestionRead, summary="Update Question")
def update_question(
    question_update: QuestionUpdate, question_id: str, session: Session = Depends(get_session)
) -> QuestionRead:
    """
    Update an existing question's information.
    """
    return service_update_question(question_update, question_id, session)


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Question")
def delete_question(question_id: str, session: Session = Depends(get_session)):
    """
    Delete a question by its ID.
    """
    return service_delete_question(question_id, session)


@router.get("/", response_model=list[QuestionRead], summary="List All Questions")
def list_questions(session: Session = Depends(get_session)) -> list[QuestionRead]:
    """
    List all questions in the system.
    """
    return service_list_questions(session)