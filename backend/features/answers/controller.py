import logging
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from database.core import get_session
from entities.users import User
from .models import AnswerCreate, AnswerRead, AnswerUpdate
from .service import (
    create_answer as service_create_answer,
    get_answer_by_id as service_get_answer_by_id,
    update_answer as service_update_answer,
    delete_answer as service_delete_answer,
    list_answers as service_list_answers
)


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/answers", tags=["answers"])

@router.post("/", response_model=AnswerRead, summary="Create Answer")
def create_answer(answer: AnswerCreate, session: Session = Depends(get_session)) -> AnswerRead:
    """
    Create a new answer in the system.
    """
    return service_create_answer(answer, session)


@router.get("/{answer_id}", response_model=AnswerRead, summary="Get Answer by ID")
def get_answer(answer_id: str, session: Session = Depends(get_session)) -> AnswerRead:
    """
    Retrieve an answer by its ID.
    """
    return service_get_answer_by_id(answer_id, session)


@router.patch("/{answer_id}", response_model=AnswerRead, summary="Update Answer")
def update_answer(
    answer_update: AnswerUpdate, answer_id: str, session: Session = Depends(get_session)
) -> AnswerRead:
    """
    Update an existing answer's information.
    """
    return service_update_answer(answer_update, answer_id, session) 


@router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Answer")
def delete_answer(answer_id: str, session: Session = Depends(get_session)):
    """
    Delete an answer by its ID.
    """
    return service_delete_answer(answer_id, session)


@router.get("/list/{question_id}", response_model=list[AnswerRead], summary="List Answers")
def list_answers(question_id: str, session: Session = Depends(get_session)) -> list[AnswerRead]:
    """
    List all answers for a specific question.
    """
    return service_list_answers(question_id, session)
     

    