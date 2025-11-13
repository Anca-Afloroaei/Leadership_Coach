import logging

from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select

from database.core import get_session
from entities.questionnaires import Questionnaire

from .models import QuestionnaireCreate, QuestionnaireRead, QuestionnaireUpdate
from .service import (
    create_questionnaire as service_create_questionnaire,
    delete_questionnaire as service_delete_questionnaire,
    get_questionnaire_by_id as service_get_questionnaire_by_id,
    list_questionnaires as service_list_questionnaires,
    update_questionnaire as service_update_questionnaire,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/questionnaires", tags=["questionnaires"])


@router.post("/", response_model=QuestionnaireRead, summary="Create Questionnaire")
def create_questionnaire(
    questionnaire: QuestionnaireCreate, session: Session = Depends(get_session)
) -> QuestionnaireRead:
    """
    Create a new questionnaire in the system.
    """
    return service_create_questionnaire(questionnaire, session)


@router.get("/{questionnaire_id}", response_model=QuestionnaireRead, summary="Get Questionnaire by ID")
def get_questionnaire(  
    questionnaire_id: str, session: Session = Depends(get_session)
) -> QuestionnaireRead:
    """
    Retrieve a questionnaire by its ID.
    """
    return service_get_questionnaire_by_id(questionnaire_id, session)


@router.patch("/{questionnaire_id}", response_model=QuestionnaireRead, summary="Update Questionnaire")
def update_questionnaire(
    questionnaire_update: QuestionnaireUpdate, questionnaire_id: str, session: Session = Depends(get_session)
) -> QuestionnaireRead:
    """
    Update an existing questionnaire's information.
    """
    return service_update_questionnaire(questionnaire_update, questionnaire_id, session)


@router.delete("/{questionnaire_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Questionnaire")
def delete_questionnaire(questionnaire_id: str, session: Session = Depends(get_session)):
    """
    Delete a questionnaire by its ID.
    """
    return service_delete_questionnaire(questionnaire_id, session)



@router.get("/", response_model=list[QuestionnaireRead], summary="List All Questionnaires")
def list_questionnaires(session: Session = Depends(get_session)) -> list[QuestionnaireRead]:
    """
    List all questionnaires in the system.
    """
    return service_list_questionnaires(session)


