from fastapi import APIRouter, Depends
from sqlmodel import Session

from database.core import get_session

from .models import QuestionWithAnswersCreate, QuestionWithAnswersRead
from .service import (
    create_question_with_answers,
    create_question_with_answers_list,
)

router = APIRouter(prefix="/question_with_answers", tags=["question_with_answers"])


@router.post("/", response_model=QuestionWithAnswersRead)
def add_question_with_answers(
    data: QuestionWithAnswersCreate,
    session: Session = Depends(get_session)
):
    return create_question_with_answers(data, session)


@router.post("/add_list", response_model=list[QuestionWithAnswersRead])
def add_questions_with_answers_list(
    data_list: list[QuestionWithAnswersCreate],
    session: Session = Depends(get_session)
):
    """
    Create multiple questions with answers in the system.
    """
    return create_question_with_answers_list(data_list, session)