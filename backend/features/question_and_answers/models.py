from typing import List

from pydantic import BaseModel


class AnswerCreateNested(BaseModel):
    answer_text: str
    score_value: int

class QuestionWithAnswersCreate(BaseModel):
    question_text: str
    competency: str
    answers: List[AnswerCreateNested]

from typing import Optional


class QuestionWithAnswersRead(BaseModel):
    question_id: str
    question_text: str
    competency: Optional[str] = None
    answers: List[dict]
