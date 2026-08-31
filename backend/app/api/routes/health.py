from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "system": settings.app_name,
        "version": settings.app_version,
    }
