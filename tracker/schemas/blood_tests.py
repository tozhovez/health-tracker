from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, validator

class BloodTestBase(BaseModel):
    test_date: datetime
    glucose_level: Optional[float] = None
    cholesterol_level: Optional[float] = None
    cortisol_level: Optional[float] = None
    melatonin_level: Optional[float] = None
    created_by: str = Field('user', min_length=1, max_length=50)

    @field_validator('created_by')
    def validate_created_by(cls, v):
        if v not in ['user', 'device', 'medical']:
            raise ValueError('created_by must be "user", "device", or "medical"')
        return v

class BloodTestCreate(BloodTestBase):
    user_uuid: UUID

class BloodTestUpdate(BaseModel):
    glucose_level: float | None = None
    cholesterol_level: float | None = None
    cortisol_level: float | None = None
    melatonin_level: float | None = None
    created_by: Optional[str] = Field(None, min_length=1, max_length=50)
    
    @field_validator('created_by')
    def validate_created_by(cls, v):
        if v is not None and v not in ['user', 'device', 'medical']:
            raise ValueError('created_by must be "user", "device", or "medical"')
        return v

class BloodTestInDB(BloodTestBase):
    user_uuid: UUID
    created_date: datetime
    updated_date: datetime

    class Config:
        from_attributes = True

class BloodTestResponse(BloodTestInDB):
    pass
