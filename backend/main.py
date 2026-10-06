from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sys
import os
import types

# Ensure that 'backend' can be imported on Vercel where 'backend' is the root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
if "backend" not in sys.modules:
    backend_mod = types.ModuleType("backend")
    backend_mod.__path__ = [current_dir]
    sys.modules["backend"] = backend_mod

from backend.core.config import settings
from backend.routers import job, story
from backend.db.database import create_tables

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_tables()
        print("Database tables created/verified successfully.")
    except Exception as e:
        print(f"Error creating database tables: {e}")
    yield

app = FastAPI(
    title="Choose Your Own Adventure Game API",
    description="api to generate cool stories",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    story.router,
    prefix=settings.API_PREFIX
)

app.include_router(
    job.router,
    prefix=settings.API_PREFIX
)


@app.get("/")
def home():
    return {
        "message": "Choose Your Own Adventure API is running 🚀"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )