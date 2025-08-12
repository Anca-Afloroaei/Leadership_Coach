import logging
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database.core import create_db_and_tables, get_session, check_db_connection
from routers import register_routers
from entities import (
    User,
    LeadershipModule,
    UserModuleProgress,
    DevelopmentPlan,
    LeadershipAssessment,
    Question,
    Answer, 
    Questionnaire,
    UserAnswer,
)


load_dotenv()

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager to create the database and tables.
    This is called when the application starts.
    """
    try:
        logger.info("Creating database and tables...")
        # Create the database and tables if they do not exist
        create_db_and_tables()
        yield
    except Exception as e:
        logger.error(f"Error during application startup: {e}")
        raise

app = FastAPI(lifespan=lifespan)


@app.get("/health", summary="Health Check")
async def health_check():
    """
    Health check endpoint to verify if the application is running.
    """
    logger.info("Health check endpoint called")
    return {"status": "ok"}


@app.get("/health/db", summary="Database Health Check")
async def db_health_check():
    """
    Endpoint to check the database connection.
    """
    try:
        check_db_connection()
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {"status": "error", "db": "not connected"}
    

# Ensure FORNTEND_URL is set in the environment with the Production URL
origins = [
    FRONTEND_URL := os.getenv("FRONTEND_URL", "http://localhost:3000"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_routers(app)
logger.info("Routers registered successfully")


if __name__ == "__main__":
    check_db_connection()