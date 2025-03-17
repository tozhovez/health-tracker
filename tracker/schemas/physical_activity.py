from typing import Optional
from uuid import UUID
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, validator

class PhysicalActivityBase(BaseModel):
    start_time: datetime = Field(default_factory=datetime.now)
    activity_duration: Optional[float] = Field(0.00, ge=0.00)
    steps: Optional[int] = Field(0, ge=0)
    calories_burned: Optional[int] = None
    heart_rate_avg: Optional[int] = None
    created_by: str = Field('user', min_length=1, max_length=50)

    @validator('created_by')
    def validate_created_by(cls, v):
        if v not in ['user', 'device', 'medical']:
            raise ValueError('created_by must be "user", "device", or "medical"')
        return v

class PhysicalActivityCreate(PhysicalActivityBase):
    user_uuid: UUID

class PhysicalActivityUpdate(BaseModel):
    activity_duration: Optional[float] = Field(None, ge=0.00)
    steps: Optional[int] = Field(None, ge=0)
    calories_burned: Optional[int] = None
    heart_rate_avg: Optional[int] = None
    created_by: Optional[str] = Field(None, min_length=1, max_length=50)

    @validator('created_by')
    def validate_created_by(cls, v):
        if v is not None and v not in ['user', 'device', 'medical']:
            raise ValueError('created_by must be "user", "device", or "medical"')
        return v

class PhysicalActivityInDB(PhysicalActivityBase):
    user_uuid: UUID
    created_date: datetime
    updated_date: datetime

    class Config:
        from_attributes = True

class PhysicalActivityResponse(PhysicalActivityInDB):
    pass
