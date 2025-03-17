from pathlib import Path
from sqlalchemy import text
from fastapi import Depends
from config import settings
from database.dbclient import AsyncDatabaseClient
from database.models import Base
import logging
logger = logging.getLogger(__name__)

# Add a flag to prevent running the initialisation many times
database_initialized = False

async def get_db_client():
    client = AsyncDatabaseClient(settings.DATABASE_URL)
    try:
        yield client
    finally:
        await client.close()


async def init_db():
    """Initialize the database: create tables and load dummy data."""
    client = AsyncDatabaseClient(settings.DATABASE_URL)
    global database_initialized
    if database_initialized:
        logger.info("Database already initialized. Skipping.")
        return
    
    try:
        async with client.engine.begin() as conn:
            # Create tables
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully.")

        # Load dummy data from SQL file
        sql_file_path = Path(__file__).parent.parent / settings.SQL_FILE_PATH

        if sql_file_path.exists():
            sql_queries = sql_file_path.read_text()
            # Splitting the SQL file into individual queries
            queries = sql_queries.split(";")
            async with client.engine.connect() as conn:
                await conn.execution_options(isolation_level="AUTOCOMMIT")
                for query in queries:
                    query = query.strip()
                    if query:
                        await conn.execute(text(query))
                        logger.info("Dummy data loaded successfully.")
                    else:
                        logger.warning(f"SQL file not found: {sql_file_path}")
                await conn.commit()
                await client.close()
        database_initialized = True
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
    
async def shutdown_db():
    client = AsyncDatabaseClient(settings.DATABASE_URL)
    await client.close()