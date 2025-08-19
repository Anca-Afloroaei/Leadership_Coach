import logging
from fastapi import HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from entities.users import User

from user_answers.service import get_user_answers_by_record_id
from models import UserResultRead


logger = logging.getLogger(__name__)

def get_user_results_by_record_id(
    user_answers_record_id: str, current_user: User, session: Session
):

    user_answers_record = get_user_answers_by_record_id(
        user_answers_record_id, current_user, session
    )

    user_answer_dict = user_answers_record.answers

    # create a empty dict to hold the competence and score
    competence_scores = {}

    # { question_id: answerid }
    # call user_answer_dict.items() on the dict in a for loop
    #

    # SQL alachemy in here to get the actual competence and the score from the questions table & answers table

    # from the key (question_id) we can get the competence
    # and from the value (answer_id) we can get the score

    # append the competence and score to the competence_scores dict


    user_results_record = UserResultRead(
        user_answers_record_id=user_answers_record.id,
        user_id=current_user.id,
        questionnaire_id=user_answers_record.questionnaire_id,
        results=competence_scores,  # This should be a dict of competence and score
        completed_at=user_answers_record.completed_at,
    )

    # to construct this below thing we need to acess the answers table and mulitple the score by 25 + %

    # Vision & Strategic Thinking : 75%
    # Communication
    # Emotional Intelligence
    # Decision-Making
    # Delegation
    # Coaching & Developing Others
    # Adaptability
    # Accountability
    # Influence & Persuasion
    # Conflict Management
    # Collaboration & Teamwork
    # Innovation & Change Leadership
    # Resilience & Stress Management
    # Ethical Leadership & Integrity
    # Results Orientation

    return UserResultsRead.model_validate(user_results_record)
