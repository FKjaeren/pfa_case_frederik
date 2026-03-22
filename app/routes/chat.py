import uuid
import structlog
from fastapi import APIRouter, HTTPException, Request, status
from google.api_core.exceptions import GoogleAPICallError, Unauthenticated, ResourceExhausted

from app.agent.agent import run_agent
from app.logging import get_logger
from app.models.schemas import ChatRequest, ChatResponse, HealthResponse
from app.config import get_settings

router = APIRouter()
logger = get_logger(__name__)


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    tags=["Ops"],
)
async def health() -> HealthResponse:
    """Returns 200 when the service is up."""
    return HealthResponse(version=get_settings().app_version)


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with the Northstar agent",
    tags=["Agent"],
    responses={
        400: {"description": "The request body is malformed."},
        403: {"description": "Your API key doesn't have the required permissions."},
        429: {"description": "You've exceeded the rate limit."},
        503: {"description": "The service may be temporarily overloaded or down."},
    },
)
async def chat(request: ChatRequest, req: Request) -> ChatResponse:
    """
    Send a message to the Northstar knowledge agent.

    - **message**: Your question (max 4 000 characters).
    - **conversation_history**: Optional list of previous turns to maintain context
      (max 20 turns, alternating user/assistant roles).

    The agent will only answer questions based on the Northstar Culinary Technologies
    knowledge base. The `in_scope` field in the response indicates whether the question
    was within the knowledge domain.
    """
    request_id = str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(request_id=request_id)

    logger.info("chat_request_received", message_length=len(request.message))

    try:
        response = await run_agent(request)
        return response
 
    except Unauthenticated:
        logger.error("gemini_auth_error")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Upstream authentication error. Please contact support.",
        )
    except ResourceExhausted:
        logger.warning("gemini_rate_limit")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="The AI service is temporarily rate-limited. Please retry in a moment.",
        )
    except GoogleAPICallError as exc:
        logger.error("gemini_api_error", message=str(exc))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Upstream API error: {exc.message}",
        )
    except Exception:
        logger.exception("unexpected_error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again.",
        )
    finally:
        structlog.contextvars.clear_contextvars()