import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from router import api_router
from config import settings
from dependencies import init_db, shutdown_db


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

# Routes
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager for managing the application's lifecycle.
    This function is called when the application starts and stops.
    It initializes the database connection on startup and handles any cleanup on shutdown.
    """
    await init_db()
    logging.info("Application start...")
    yield
    logging.info("Application shutdown...")
    await shutdown_db()

app = FastAPI(
    lifespan=lifespan,
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Health Tracker API",
        "docs": "/docs",
        "redoc_url" :"/redoc",
        "version": settings.PROJECT_VERSION
    }


# Error Handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6565)
