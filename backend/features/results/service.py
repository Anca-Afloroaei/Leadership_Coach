import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from entities.answers import Answer
from entities.questions import Question
from entities.users import User
from features.user_answers.service import get_user_answers_by_record_id

from .models import UserResultRead

logger = logging.getLogger(__name__)

def get_user_results_by_record_id(
    user_answers_record_id: str, current_user: User, session: Session
):

    # Fetch the user's answers record with auth checks
    user_answers_record = get_user_answers_by_record_id(
        user_answers_record_id, current_user, session
    )

    user_answer_dict = user_answers_record.answers

    if not user_answer_dict:
        # No answers yet; return empty results
        return UserResultRead(
            user_answers_record_id=user_answers_record.id,
            user_id=current_user.id,
            questionnaire_id=user_answers_record.questionnaire_id,
            results={},
            completed_at=user_answers_record.completed_at,
        )

    question_ids = list(user_answer_dict.keys())

    # Fetch questions to get competencies
    questions = session.exec(
        select(Question).where(Question.id.in_(question_ids))
    ).all()
    competency_by_qid = {q.id: (q.competency or "Unknown") for q in questions}

    # Fetch all answers for these questions to compute per-question max scores
    all_answers = session.exec(
        select(Answer).where(Answer.question_id.in_(question_ids))
    ).all()

    # Compute max score per question
    max_score_by_qid: dict[str, int] = {}
    for ans in all_answers:
        prev = max_score_by_qid.get(ans.question_id)
        if prev is None or ans.score_value > prev:
            max_score_by_qid[ans.question_id] = ans.score_value

    # Map selected answers (by id) to their question and score
    selected_answer_ids = list(user_answer_dict.values())
    selected_answers = session.exec(
        select(Answer).where(Answer.id.in_(selected_answer_ids))
    ).all()
    selected_by_qid: dict[str, int] = {}
    for ans in selected_answers:
        selected_by_qid[ans.question_id] = ans.score_value

    # Aggregate per competency
    sum_selected: dict[str, float] = {}
    sum_max: dict[str, float] = {}

    for qid in question_ids:
        comp = competency_by_qid.get(qid)
        if not comp:
            continue
        selected = float(selected_by_qid.get(qid, 0))
        max_score = float(max_score_by_qid.get(qid, 0))
        if max_score <= 0:
            # Skip malformed questions without scoring
            continue
        sum_selected[comp] = sum_selected.get(comp, 0.0) + selected
        sum_max[comp] = sum_max.get(comp, 0.0) + max_score

    # Compute percentages (0-100)
    competence_scores: dict[str, float] = {}
    for comp, max_total in sum_max.items():
        sel_total = sum_selected.get(comp, 0.0)
        pct = 0.0
        if max_total > 0:
            pct = (sel_total / max_total) * 100.0
        # Clamp and round to whole numbers for UI
        pct = max(0.0, min(100.0, round(pct)))
        competence_scores[comp] = pct

    return UserResultRead(
        user_answers_record_id=user_answers_record.id,
        user_id=current_user.id,
        questionnaire_id=user_answers_record.questionnaire_id,
        results=competence_scores,
        completed_at=user_answers_record.completed_at,
    )
