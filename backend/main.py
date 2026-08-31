from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes.health import router as health_router
from app.api.routes.auth import router as auth_router
from app.core.config import get_settings
from app.core.database import init_db

settings = get_settings()
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = (BASE_DIR / ".." / "frontend").resolve()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API inicial do Sistema de Gestão.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


@app.on_event("startup")
def on_startup() -> None:
    init_db()
