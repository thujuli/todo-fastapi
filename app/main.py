from fastapi import FastAPI
from app.core.config import settings
from app.api.api_v1.api import api_router

# migration used alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.project_name, openapi_url=f"{settings.api_v1_str}/openapi.json"
)

app.include_router(api_router, prefix=settings.api_v1_str)
