import logging
from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlmodel import Session

from database.core import get_session
from entities.development_plans import DevelopmentPlan
from entities.users import User
from features.auth.service import get_current_user

from .models import (
    DevelopmentPlanCreate,
    DevelopmentPlanRead,
    DevelopmentPlanSummaryRead,
    GeneratePlanRequest,
    GeneratePlanResponse,
)
from .service import (
    create_development_plan as service_create_development_plan,
    delete_development_plan as service_delete_development_plan,
    generate_development_plan_from_ai as service_generate_plan,
    get_development_plan_by_id as service_get_development_plan_by_id,
    get_development_plan_for_user_answers as service_get_development_plan_for_user_answers,
    get_development_plan_pdf_for_user_answers as service_get_development_plan_pdf_for_user_answers,
    list_development_plans_for_user as service_list_plans_for_user,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/devplans", tags=["development_plans"])

@router.post("/", response_model=DevelopmentPlanRead, summary="Create Development Plan")
def create_development_plan(
    development_plan: DevelopmentPlanCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DevelopmentPlanRead:
    """Create a new Development Plan for the authenticated user."""
    if development_plan.user_id != current_user.id:
        logger.warning(
            "User %s attempted to create a development plan for user %s",
            current_user.id,
            development_plan.user_id,
        )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Access")

    return service_create_development_plan(development_plan, session)


@router.get("/{development_plan_id}", response_model=DevelopmentPlanRead, summary="Get Development Plan by ID")
def get_development_plan(
    development_plan_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DevelopmentPlanRead:
    """Retrieve a Development Plan by its ID for the authenticated user."""
    plan = service_get_development_plan_by_id(development_plan_id, session)
    if plan.user_id != current_user.id:
        logger.warning(
            "User %s attempted to access development plan %s belonging to %s",
            current_user.id,
            development_plan_id,
            plan.user_id,
        )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Access")
    return plan


@router.delete(
    "/{development_plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Development Plan",
)
def delete_development_plan(
    development_plan_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> None:
    """Delete a Development Plan by its ID for the authenticated user."""
    plan = service_get_development_plan_by_id(development_plan_id, session)
    if plan.user_id != current_user.id:
        logger.warning(
            "User %s attempted to delete development plan %s belonging to %s",
            current_user.id,
            development_plan_id,
            plan.user_id,
        )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Access")

    service_delete_development_plan(development_plan_id, session)
    return None


@router.post("/generate", response_model=GeneratePlanResponse, summary="Generate a Development Plan using AI")
def generate_development_plan(
    payload: GeneratePlanRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> GeneratePlanResponse:
    return service_generate_plan(payload, current_user, session)


@router.get(
    "/user_answers/{user_answers_record_id}",
    response_model=GeneratePlanResponse,
    summary="Get Development Plan linked to a user answers record",
)
def get_plan_for_user_answers(
    user_answers_record_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> GeneratePlanResponse:
    return service_get_development_plan_for_user_answers(
        user_answers_record_id, current_user, session
    )


@router.get(
    "/user_answers/{user_answers_record_id}/pdf",
    response_class=StreamingResponse,
    summary="Download development plan PDF for a user answers record",
)
def download_plan_pdf(
    user_answers_record_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> StreamingResponse:
    pdf_bytes, filename = service_get_development_plan_pdf_for_user_answers(
        user_answers_record_id, current_user, session
    )
    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"',
    }
    return StreamingResponse(BytesIO(pdf_bytes), media_type="application/pdf", headers=headers)


@router.get(
    "/",
    response_model=list[DevelopmentPlanSummaryRead],
    summary="List development plans for the authenticated user",
)
def list_user_development_plans(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> list[DevelopmentPlanSummaryRead]:
    return service_list_plans_for_user(current_user, session)
