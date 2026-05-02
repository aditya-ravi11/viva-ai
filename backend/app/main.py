"""FastAPI application entrypoint.

Wires up routers, middleware, lifespan events. The hot path (live interview
session) lives in app.services.voice_loop and is invoked via WebSocket
endpoints registered here.
"""
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import health


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Startup / shutdown hooks. Open DB pools, warm prosody model, etc."""
    # TODO: warm up DB pool, preload openSMILE config
    yield
    # TODO: close pools, flush queues


app = FastAPI(
    title="AI Mock Interviewer",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
