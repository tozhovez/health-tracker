from fastapi import APIRouter
from api.users import users_router
from api.physical_activity import physical_activity_router
from api.sleep_activity import sleep_activity_router
from api.blood_tests import blood_tests_router
from api.bio_metrics import bio_metrics_router
from api.health import health_router

# API endpoints:
#     users, physical_activity, sleep_activity,
#     blood_tests, bio_metrics, health

api_router = APIRouter()
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(
    blood_tests_router,
    prefix="/blood-tests",
    tags=["blood-tests"]
    )

api_router.include_router(
    bio_metrics_router,
    prefix="/bio-metrics",
    tags=["bio-metrics"]
    )

api_router.include_router(
    physical_activity_router,
    prefix="/physical-activity",
    tags=["physical-activity"]
    )

api_router.include_router(
    sleep_activity_router,
    prefix="/sleep-activity",
    tags=["sleep-activity"]
    )

api_router.include_router(
    health_router,
    prefix="/health-score",
    tags=["health-score"]
    )


