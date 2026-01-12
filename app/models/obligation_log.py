import uuid
from enum import Enum

from sqlalchemy import (
    String,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.db.base import Base

class ObligationEventType(str, Enum):
    CREATED = "CREATED"
    COMPLETED = "COMPLETED"
    MARKED_LATE = "MARKED_LATE"
    CANCELLED = "CANCELLED"
    NOTE_ADDED = "NOTE_ADDED"
    CORRECTED = "CORRECTED"


class ObligationLog(Base):
    __tablename__ = "obligation_logs"

    obligation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("obligations.id",ondelete="RESTRICT"),
        nullable=False
    )

    actor_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )

    event_type: Mapped[ObligationEventType] = mapped_column(
        SQLEnum(ObligationEventType, name = "obligation_event_type"),
        nullable=False
    )

    notes: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    event_metadata: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True
    )
    
    obligation = relationship("Obligation")
    actor = relationship("User")
