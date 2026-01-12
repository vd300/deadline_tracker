from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class CreateObligationRequest(BaseModel):
    title: str
    description: str
    due_date: datetime
    owner_user_id: UUID
    organization_id: UUID
    client_id: UUID