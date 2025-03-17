import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from database.dbclient import AsyncDatabaseClient, get_db, refresh_db
from database.models import Base
from config import settings
from unittest.mock import patch, AsyncMock
import logging

logger = logging.getLogger(__name__)

# Sample Pydantic model for testing
class SampleModel(BaseModel):
    id: int
    name: str

# Sample SQLAlchemy model for testing
class SampleSQLModel(Base):
    __tablename__ = 'sample'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

@pytest.fixture
async def async_db_client():
    client = AsyncDatabaseClient(settings.DATABASE_URL)
    yield client
    await client.close()

@pytest.mark.asyncio
async def test_get_session(async_db_client):
    session = await async_db_client.get_session()
    assert isinstance(session, AsyncSession)

@pytest.mark.asyncio
async def test_create(async_db_client):
    data = SampleModel(id=1, name="Test")
    created_item = await async_db_client.create(SampleSQLModel, data)
    assert created_item.id == data.id
    assert created_item.name == data.name

@pytest.mark.asyncio
async def test_close(async_db_client):
    await async_db_client.close()
    assert async_db_client.engine.pool is None

@pytest.mark.asyncio
async def test_get_db():
    async for session in get_db():
        assert isinstance(session, AsyncSession)

@pytest.mark.asyncio
@patch("database.dbclient.Path.read_text", return_value="SELECT 1;")
@patch("database.dbclient.AsyncDatabaseClient.engine.connect", new_callable=AsyncMock)
async def test_refresh_db(mock_connect, mock_read_text):
    mock_conn = mock_connect.return_value.__aenter__.return_value
    await refresh_db()
    mock_conn.execute.assert_called_with(text("SELECT 1"))
    mock_conn.commit.assert_called_once()
    logger.info.assert_called_with("refresh continuous aggregate successfully.")