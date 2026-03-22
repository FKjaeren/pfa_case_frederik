from google import genai
from app.config import get_settings
from fastapi import FastAPI, Request, status
from app.routes.chat import router

settings = get_settings()


app = FastAPI(
    title="Northstar Culinary Technologies — Knowledge Agent",
    description=(
        "A conversational AI agent that answers questions about "
        "Northstar Culinary Technologies using a curated knowledge base. "
        "Questions outside the knowledge domain are gracefully declined."
    ),
    version=settings.app_version,
    contact={"name": "Northstar Engineering"},
    license_info={"name": "Proprietary"},
)

app.include_router(router, prefix="/api/v1")
