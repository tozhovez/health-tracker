from typing import Optional
from uuid import UUID
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, validator

class SleepActivityBase(BaseModel):
    start_time: datetime = Field(default_factory=datetime.now)
    sleep_duration: float = Field(0.00, ge=0.00)
    sleep_quality: int = Field(1, ge=1, le=10)
    created_by: str = Field('user', min_length=1, max_length=50)

    @validator('created_by')
    def validate_created_by(cls, v):
        if v not in ['user', 'device', 'medical']:
            raise ValueError('created_by must be "user", "device", or "medical"')
        return v

class SleepActivityCreate(SleepActivityBase):
    user_uuid: UUID

class SleepActivityUpdate(BaseModel):
    sleep_duration: Optional[float] = Field(None, ge=0.00)
    sleep_quality: Optional[int] = Field(None, ge=1, le=10)
    created_by: Optional[str] = Field(None, min_length=1, max_length=50)

    @validator('created_by')
    def validate_created_by(cls, v):
        if v is not None and v not in ['user', 'device', 'medical']:
            raise ValueError('created_by must be "user", "device", or "medical"')
        return v

class SleepActivityInDB(SleepActivityBase):
    user_uuid: UUID
    created_date: datetime
    updated_date: datetime

    class Config:
        from_attributes = True

class SleepActivityResponse(SleepActivityInDB):
    pass
