import logging

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from entities.leadership_assessments import LeadershipAssessment
from entities.users import User

from .models import LeadershipAssessmentCreate, LeadershipAssessmentRead

logger = logging.getLogger(__name__)

# def create_assessment(assessment: LeadershipAssessmentCreate, session: Session, current_user: User) -> LeadershipAssessmentRead:
def create_assessment(assessment: LeadershipAssessmentCreate, session: Session) -> LeadershipAssessmentRead:
    """
    Create a new Leadership Assessment in the system.
    """
    new_assessment = LeadershipAssessment(
        # user_id=assessment.current_user.id,
        user_id=assessment.user_id,
        self_rating=assessment.self_rating,
        assessment_rating=assessment.assessment_rating
    )
    session.add(new_assessment)
    session.commit()
    session.refresh(new_assessment)
    logger.info(f"Leadership Assessment created: {new_assessment.id}")
    return new_assessment

    # try:
        # new_assessment = LeadershipAssessment(
        #     # user_id=assessment.current_user.id,
        #     user_id=assessment.current_user,
        #     self_rating=assessment.self_rating,
        #     assessment_rating=assessment.assessment_rating
        # )
        # session.add(new_assessment)
        # session.commit()
        # session.refresh(new_assessment)
        # logger.info(f"Leadership Assessment created: {new_assessment.id}")
        # return LeadershipAssessmentRead.from_attributes(new_assessment)
    # except IntegrityError as e:
    #     session.rollback()
    #     logger.error(f"Integrity error while creating assessment: {e}")
    #     raise HTTPException(status_code=400, detail="Integrity error occurred")
    # except Exception as e:
    #     session.rollback()
    #     logger.error(f"Error creating assessment: {e}")
    #     raise HTTPException(status_code=500, detail="Internal server error")


def get_leadrship_assessment_by_id(assessment_id, session) -> LeadershipAssessmentRead:
    """
    Retrieve a Leadership Assessment by its ID.
    """
    statement = select(LeadershipAssessment).where(LeadershipAssessment.id == assessment_id)
    assessment = session.exec(statement).first()
    if not assessment:
        logger.error(f"Leadership Assessment with ID {assessment_id} not found")
        raise HTTPException(status_code=404, detail="Leadership Assessment not found")
    logger.info(f"Leadership Assessment retrieved: {assessment.id}")
    return LeadershipAssessmentRead.model_validate(assessment)  # Assuming LeadershipAssessmentRead has a model_validate method to convert the model



def delete_leadrship_assessment(assessment_id, session) -> None:
    """
    Delete a Leadership Assessment by its ID.
    """
    statement = select(LeadershipAssessment).where(LeadershipAssessment.id == assessment_id)
    assessment = session.exec(statement).first()
    if not assessment:
        logger.error(f"Leadership Assessment with ID {assessment_id} not found")
        raise HTTPException(status_code=404, detail="Leadership Assessment not found")
    session.delete(assessment)
    session.commit()
    logger.info(f"Leadership Assessment with ID {assessment_id} deleted successfully")
    return None





