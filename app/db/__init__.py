from app.db.base import Base

# Import all models here so Alembic can see them later
from app.models.organization import Organization 
from app.models.user import User
from app.models.client import Client

#print(Base.metadata.tables)