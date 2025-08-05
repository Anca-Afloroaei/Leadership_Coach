from uuid import uuid4
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timezone


class DevelopmentPlan(SQLModel, table=True):
    """
    Development Plan model representing a development plan in the system.
    This model is used to store development plan information in the database.
    """

    __tablename__ = "development_plans"
    id: str = Field(default_factory=lambda: uuid4().hex, primary_key=True, index=True)
    user_id: str = Field(
        sa_column=Column(String, ForeignKey("users.id"), nullable=False)
    )
    goal: str = Field(sa_column=Column(String, nullable=False))
    description: str = Field(
        sa_column=Column(String, nullable=False)
    )  # Optional details/description of the goal
    start_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            nullable=False,
        ),
    )
    end_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            nullable=False,
        ),
    )
    status: str = Field(
        sa_column=Column(String, nullable=False)
    )  # e.g: "In Progress", "Completed", "On Hold"
    progress: int = Field(
        default=0, sa_column=Column(Integer, nullable=False)
    )  # Progress percentage (0-100)
    resources: str = Field(
        sa_column=Column(String, nullable=True)
    )  # Optional resources
    challenges: str = Field(
        sa_column=Column(String, nullable=True)
    )  # Optional challenges
    next_steps: str = Field(
        sa_column=Column(String, nullable=True)
    )  # Optional next steps to take
    action_items: str = Field(
        sa_column=Column(String, nullable=False)
    )  # Action items to be completed
    target_date: datetime = Field(
        DateTime(timezone=True), nullable=False
    )  # Target date for the action items
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            nullable=False,
        ),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc),
            nullable=False,
        ),
    )

    # plan_details: str = Field(sa_column=Column(String, nullable=False))  # Detailed description of the plan
    # completion_date: datetime = Field(
    #     default_factory=lambda: datetime.now(timezone.utc),
    #     sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=True),
    # )  # Optional completion date if the plan is completed
    # last_updated: datetime = Field(
    #     default_factory=lambda: datetime.now(timezone.utc),
    #     sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=datetime.now, nullable=False),
    # )  # Last updated timestamp

    # priority: str = Field(sa_column=Column(String, nullable=False))  # e.g: "High", "Medium", "Low"
    # created_at: datetime = Field(
    #     default_factory=lambda: datetime.now(timezone.utc),
    #     sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False),
    # )
    # updated_at: datetime = Field(
    #     default_factory=lambda: datetime.now(timezone.utc),
    #     sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=datetime.now, nullable=False),
    # )

    # # Optional fields for additional information
    # mentor_id: str = Field(sa_column=Column(String, ForeignKey("users.id"), nullable=True))  # Optional mentor assigned to the plan
    # coach_id: str = Field(sa_column=Column(String, ForeignKey("users.id"), nullable=True))  # Optional coach assigned to the plan
    # # Optional feedback from mentors or coaches
    # feedback: str = Field(sa_column=Column(String, nullable=True))  # Optional feedback from mentors or coaches

    # action_items: str = Field(sa_column=Column(String, nullable=False))

    # plan_details: str = Field(sa_column=Column(String, nullable=False))
