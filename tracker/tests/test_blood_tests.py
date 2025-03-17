import pytest
from httpx import AsyncClient
from fastapi import status
from uuid import uuid4
from datetime import datetime
from schemas.blood_tests import BloodTestCreate, BloodTestUpdate

from main import app  # Assuming your FastAPI app is in main.py

@pytest.mark.asyncio
async def test_create_blood_tests():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        blood_test_data = {
            "user_id": str(uuid4()),
            "test_date": datetime.now().isoformat(),
            "test_results": "Some test results"
        }
        response = await ac.post("/blood_tests/", json=blood_test_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["test_results"] == blood_test_data["test_results"]

@pytest.mark.asyncio
async def test_read_all_blood_tests_by_user():
    user_uuid = str(uuid4())
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/blood_tests/{user_uuid}")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_read_blood_tests_by_user_by_date():
    user_uuid = str(uuid4())
    test_date = datetime.now().isoformat()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/blood_tests/{user_uuid}/{test_date}")
    if response.status_code == status.HTTP_404_NOT_FOUND:
        assert response.json()["detail"] == "Blood tests not found"
    else:
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_update_blood_tests():
    user_uuid = str(uuid4())
    test_date = datetime.now().isoformat()
    update_data = {
        "test_results": "Updated test results"
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.patch(f"/blood_tests/{user_uuid}/{test_date}/update", json=update_data)
    if response.status_code == status.HTTP_404_NOT_FOUND:
        assert response.json()["detail"] == "Blood tests not found"
    else:
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["test_results"] == update_data["test_results"]

@pytest.mark.asyncio
async def test_delete_blood_tests():
    user_uuid = str(uuid4())
    test_date = datetime.now().isoformat()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/blood_tests/{user_uuid}/delete", params={"test_date": test_date})
    if response.status_code == status.HTTP_404_NOT_FOUND:
        assert response.json()["detail"] == "Blood tests not found"
    else:
        assert response.status_code == status.HTTP_200_OK