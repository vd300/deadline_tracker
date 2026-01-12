from app.models.obligation import ObligationStatus

def can_complete(status:ObligationStatus) -> bool:
    return status in {ObligationStatus.PENDING, ObligationStatus.LATE}

def can_mark_late(status:ObligationStatus) -> bool:
    return status == ObligationStatus.PENDING

def can_cancel(status:ObligationStatus) -> bool:
    return status in {ObligationStatus.PENDING, ObligationStatus.LATE}