from app.db.base import Base

# Import all models here so Alembic can see them later
from app.models.organization import Organization 

print(Base.metadata.tables)