import logging

from fastapi import HTTPException
from sqlalchemy.exc import OperationalError
from sqlmodel import Session, SQLModel, create_engine, text

from config import settings

logger = logging.getLogger(__name__)


connect_args = {}
if settings.DATABASE_URL.startswith("postgresql"):
    # "prefer" keeps SSL in production while allowing non-SSL local dev
    connect_args = {"sslmode": "prefer"}

engine = create_engine(
    settings.DATABASE_URL,
    # connect_args={"sslmode": "require"},
    connect_args=connect_args,
    echo=False,
    pool_pre_ping=True,  # Validate connections before using them
    pool_recycle=3600,  # Recycle connections after 1 hour (before they timeout)
    pool_size=20,
    max_overflow=20,
)


def _ensure_development_plan_schema() -> None:
    """Ensure new development_plan columns exist without relying on external migrations."""
    with engine.begin() as conn:
        conn.exec_driver_sql(
            """
            ALTER TABLE development_plans
            ADD COLUMN IF NOT EXISTS user_answers_record_id VARCHAR(32)
            """
        )
        conn.exec_driver_sql(
            """
            ALTER TABLE development_plans
            ADD COLUMN IF NOT EXISTS plan_markdown TEXT
            """
        )
        conn.exec_driver_sql(
            """
            ALTER TABLE development_plans
            ALTER COLUMN plan_markdown SET DEFAULT ''
            """
        )
        conn.exec_driver_sql(
            """
            UPDATE development_plans
            SET plan_markdown = ''
            WHERE plan_markdown IS NULL
            """
        )
        conn.exec_driver_sql(
            """
            ALTER TABLE development_plans
            ALTER COLUMN plan_markdown SET NOT NULL
            """
        )
        conn.exec_driver_sql(
            """
            CREATE INDEX IF NOT EXISTS ix_development_plans_user_answers_record_id
            ON development_plans (user_answers_record_id)
            """
        )
        conn.exec_driver_sql(
            """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1
                    FROM information_schema.table_constraints
                    WHERE constraint_name = 'development_plans_user_answers_record_id_fkey'
                      AND table_name = 'development_plans'
                ) THEN
                    ALTER TABLE development_plans
                    ADD CONSTRAINT development_plans_user_answers_record_id_fkey
                    FOREIGN KEY (user_answers_record_id)
                    REFERENCES user_answers(id)
                    ON DELETE SET NULL;
                END IF;
            END;
            $$
            """
        )


def create_db_and_tables():
    """
    Create the database and tables if they do not exist.
    This function should be called at the start of the application.
    """
    SQLModel.metadata.create_all(engine)
    try:
        _ensure_development_plan_schema()
    except Exception as exc:
        logger.error("Failed to enforce development plan schema: %s", exc)
        raise


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
            except HTTPException:
                session.rollback()
                raise
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
        except HTTPException:
            raise
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