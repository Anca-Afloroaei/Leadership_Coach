from sqlmodel import SQLModel, Session, create_engine, text
from sqlalchemy.exc import OperationalError
import logging

from config import settings

logger = logging.getLogger(__name__)


engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"sslmode": "require"},
    echo=False,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=20,
)


def create_db_and_tables():
    """
    Create the database and tables if they do not exist.
    This function should be called at the start of the application.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    FastAPI dependency that yields a new SQLModel Session
    and commits/rolls back automatically when the request ends.
    Includes proper error handling and connection cleanup with retry logic.
    """
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            session = Session(engine)
            try:
                yield session
                session.commit()
                return
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
        except OperationalError as e:
            retry_count += 1
            logger.warning(f"Database connection attempt {retry_count} failed: {e}")
            if retry_count >= max_retries:
                logger.error("Maximum database connection retries exceeded")
                raise
            # Wait a bit before retrying
            import time

            time.sleep(0.5 * retry_count)
        except Exception as e:
            logger.error(f"Unexpected database error: {e}")
            raise


def check_db_connection():
    """
    Check if the database connection is alive.
    This can be used to verify the connection status at any point.
    """
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
        logger.info("Database connection is alive")
    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while checking database connection: {e}")
        raise


