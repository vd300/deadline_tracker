import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import(
    String,
    DateTime,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base

class ObligationStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    LATE = "LATE"
    CANCELLED = "CANCELLED"


class Obligation(Base):
    __tablename__ = "obligations"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id",ondelete="RESTRICT"),
        nullable=False
    )

    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("clients.id",ondelete="RESTRICT")
    )

    owner_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    due_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    status: Mapped[ObligationStatus] = mapped_column(
        SQLEnum(ObligationStatus, name="obligation_status"),
        nullable=False,
        default=ObligationStatus.PENDING,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    organization = relationship("Organization")
    client = relationship("Client")
    owner = relationship("User")
    