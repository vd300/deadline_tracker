from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
import uuid
from datetime import datetime, timezone
from app.core.database import getdb
from app.schemas.obligations import CreateObligationRequest 
from app.models.obligation_log import ObligationLog, ObligationEventType
from app.models.obligation import Obligation, ObligationStatus
from app.domain.obligations import can_complete, can_mark_late, can_cancel

router = APIRouter(prefix="/api/v1/obligations", tags=["obligations"])

@router.post("")
def create_obligation(
    payload: CreateObligationRequest,
    db: Session = Depends(getdb)    
):
    obligation = Obligation(
        id = uuid.uuid4(),
        client_id = payload.client_id,
        owner_user_id = payload.owner_user_id,
        organization_id = payload.organization_id,
        title = payload.title,
        description = payload.description,
        due_at = payload.due_date,
        status = ObligationStatus.PENDING,
    )
    db.add(obligation)
    db.flush()

    log =  ObligationLog(
        obligation_id = obligation.id,
        event_type = ObligationEventType.CREATED,
        actor_user_id = payload.owner_user_id,
        event_metadata = {},
    )
    db.add(log)

    db.commit()
    db.refresh(obligation)
    return obligation

@router.post("/{obligation_id}/complete")
def complete_obligation(
    obligation_id: UUID,
    db: Session = Depends(getdb)
):
    obligation = db.get(Obligation, obligation_id)
    if not obligation:
        raise HTTPException(status_code=404, detail="Obligation not found")
    
    if not can_complete(obligation.status):
        raise HTTPException(status_code=400, detail="Obligation cannot be completed in its current status")
    
    obligation.status = ObligationStatus.COMPLETED
    obligation.completed_at = datetime.now(timezone.utc)


    db.commit()
    db.refresh(obligation)
    return obligation