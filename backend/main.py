from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    # Local development from project root
    from backend.core.config import settings
    from backend.routers import job, story
    from backend.db.database import create_tables
except ModuleNotFoundError:
    # Vercel deployment from backend directory
    from core.config import settings
    from routers import job, story
    from db.database import create_tables


create_tables()


app = FastAPI(
    title="Choose Your Own Adventure Game API",
    description="api to generate cool stories",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
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