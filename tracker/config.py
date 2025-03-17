import os
from dotenv import load_dotenv
load_dotenv()
class Settings:
    PROJECT_NAME: str = "Health Tracker API"
    PROJECT_VERSION: str = "1.0.0"
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "docker")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "docker")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "postgresql")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "dev_health")
    DATABASE_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    #"postgresql+asyncpg://docker:docker@0.0.0.0:6432/dev_health"
    SQL_START: str = "infra/start.sql"
    SQL_FILE_PATH: str = "infra/dummy_data.sql"
    SQL_REFRESH: str = "infra/refresh.sql"
    FRONTEND_DIR: str = "frontend/dashboard"
settings = Settings()
