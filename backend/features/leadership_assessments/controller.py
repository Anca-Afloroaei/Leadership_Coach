import logging

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from database.core import get_session
from entities.leadership_assessments import LeadershipAssessment
from entities.users import User

from .models import LeadershipAssessmentCreate, LeadershipAssessmentRead
from .service import (
    create_assessment as service_create_leadrship_assessment,
    delete_leadrship_assessment as service_delete_leadrship_assessment,
    get_leadrship_assessment_by_id as service_get_leadrship_assessment_by_id,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/assessements", tags=["assessements"])

@router.post("/", response_model=LeadershipAssessmentRead, summary="Create Leadership Assessment")
# def create_assessment(assessment: LeadershipAssessmentCreate, session: Session = Depends(get_session), current_user: User=Depends(get_current_user)) -> LeadershipAssessmentRead:
def create_assessment(assessment: LeadershipAssessmentCreate, session: Session = Depends(get_session)) -> LeadershipAssessmentRead:

    """
    Create a new Leadership Assessment in the system.
    """
    return service_create_leadrship_assessment(assessment, session)


@router.get("/{assessment_id}", response_model=LeadershipAssessmentRead, summary="Get Leadership Assessment by ID")
def get_assessment(assessment_id: str, session: Session = Depends(get_session)) -> LeadershipAssessmentRead:
    """
    Retrieve a Leadership Assessment by its ID.
    """
    return service_get_leadrship_assessment_by_id(assessment_id, session)



@router.delete("/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Leadership Assessment")
def delete_assessment(assessment_id: str, session: Session = Depends(get_session)):
    """
    Delete a Leadership Assessment by its ID.
    """
    return service_delete_leadrship_assessment(assessment_id, session)