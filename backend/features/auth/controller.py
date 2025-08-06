"""
Authentication controller handling user registration and session management.

This module provides HTTP endpoints for user authentication workflows including:
- User registration with immediate session creation
- Login with JWT-based session tokens
- Session refresh to extend active sessions
- Logout with proper cookie cleanup
- Session status validation for frontend timers

All endpoints follow RESTful conventions and use HTTP-only cookies for
secure token storage, preventing XSS attacks while maintaining usability.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from config import settings
from database.core import get_session
from entities import User
from ..users.models import UserCreate, UserRead
from .service import (
    create_user_account,
    authenticate_user,
    create_session_token,
    refresh_user_session,
    get_current_user,
    validate_session_status,
)


def _set_auth_cookie(response: JSONResponse, token: str) -> None:
    """
    Set the authentication cookie in the response.
    This function configures the cookie with security settings based on the environment.
    It ensures the cookie is HTTP-only, secure in production, and has a defined expiration.
    """
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )


def _create_auth_response(content: dict, token: str) -> JSONResponse:
    """
    Create a standardized JSON response for authentication endpoints.
    """
    response = JSONResponse(content=content)
    _set_auth_cookie(response, token)
    return response


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
def signup(
    user_in: UserCreate,
    session: Session = Depends(get_session),
):
    """
    Register a new user and create an authentication session.
    This endpoint creates a new user account and immediately generates
    a session token for the user, allowing them to be logged in right after registration.
    """
    user = create_user_account(user_in, session)
    access_token = create_session_token(user.id)

    return _create_auth_response(
        content={
            "user": UserRead.model_validate(user).model_dump(mode="json"),
            "message": "Account created successfully",
        },
        token=access_token,
    )


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    """
    Authenticate user and create session token.
    """
    # Authenticate user
    user = authenticate_user(form_data.username, form_data.password, session)

    # Create session token
    access_token = create_session_token(user.id)

    # Create response with session cookie
    return _create_auth_response(
        content={"message": "Login successful"},
        token=access_token,
    )


@router.post("/refresh")
def refresh_session(
    current_user: User = Depends(get_current_user),
):
    """
    Refresh the current user's session by generating a new token.
    This endpoint is used to extend the session expiration without requiring
    the user to log in again.
    """
    # Generate fresh token with extended expiration
    access_token = refresh_user_session(current_user.id)

    # Replace existing cookie with new token
    return _create_auth_response(
        content={"message": "Session refreshed successfully"},
        token=access_token,
    )


@router.post("/logout")
def logout():
    """
    Invalidate the current session by clearing the authentication cookie.
    This endpoint is called when the user explicitly logs out.
    Returns:
        JSON response confirming logout with cleared cookie
    """
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie("access_token", path="/")
    return response


@router.get("/session-status")
def get_session_status(
    current_user: User = Depends(get_current_user),
):
    """
    Validate the current user's session status.
    Used by frontend to check if the user is still logged in
    and to manage session timers.
    """
    return validate_session_status(current_user.id)