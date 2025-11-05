from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import Optional
import redis.asyncio as redis
from .core.config import settings


# --------------------------------------------------
# Custom state object for typed attribute access
# --------------------------------------------------
class AppState:
    redis: Optional[redis.Redis] = None


# --------------------------------------------------
# Lifespan handler for startup/shutdown
# --------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Attach state instance (so `.state.redis` is recognized)
    app.state = AppState()

    # --- Startup ---
    app.state.redis = redis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )

    try:
        await app.state.redis.ping()
        print("Redis connected")
    except Exception as e:
        print(f"Redis connection failed: {e}")

    yield  # Run the app

    # --- Shutdown ---
    if app.state.redis:
        await app.state.redis.close()
        print("Redis closed")


# --------------------------------------------------
# Initialize FastAPI app with lifespan
# --------------------------------------------------
app = FastAPI(title="Eco-Mind A2A Agent", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Eco-Mind Agent is running"}


# --------------------------------------------------
# Helper to safely access Redis
# --------------------------------------------------
def get_redis() -> redis.Redis:
    redis_client = getattr(app.state, "redis", None)
    if not redis_client:
        raise RuntimeError("Redis not initialized")
    return redis_client
