import logging
from sqlmodel import Session
from entities.questions import Question
from entities.answers import Answer
from .models import QuestionWithAnswersCreate, QuestionWithAnswersRead

logger = logging.getLogger(__name__)

def create_question_with_answers(data: QuestionWithAnswersCreate, session: Session) -> QuestionWithAnswersRead:
    question = Question(
        question_text=data.question_text,
        competency=data.competency
    )
    session.add(question)
    session.commit()
    session.refresh(question)

    # Fetch ID of the newly created question

    # Add answers to the database
    for ans in data.answers:
        answer = Answer(
            question_id=question.id,
            answer_text=ans.answer_text,
            score_value=ans.score_value
        )
        session.add(answer)
    session.commit()

    # Fetch the question and its answers from the database
    db_question = session.get(Question, question.id)
    from sqlmodel import select
    db_answers = session.exec(select(Answer).where(Answer.question_id == question.id)).all()

    answers_data = [
        {"id": a.id, "answer_text": a.answer_text, "score_value": a.score_value} for a in db_answers
    ]
    logger.info(f"Question and answers created: {db_question.id}")
    return QuestionWithAnswersRead(
        question_id=db_question.id,
        question_text=db_question.question_text,
        competency=db_question.competency,  # Use 'competency' from the model
        answers=answers_data
    )


def create_question_with_answers_list(data_list: list[QuestionWithAnswersCreate], session: Session) -> list[QuestionWithAnswersRead]:
    results = []
    for data in data_list:
        result = create_question_with_answers(data, session)
        results.append(result)
    return results
