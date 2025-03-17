from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, validator
from decimal import Decimal

class BioMetricBase(BaseModel):
    height: Optional[Decimal] = Field(None, gt=0)
    weight: Optional[Decimal] = Field(None, gt=0)
    recorded: datetime = Field(default_factory=datetime.now)

class BioMetricCreate(BioMetricBase):
    user_uuid: UUID

class BioMetricUpdate(BaseModel):
    height: Optional[Decimal] = Field(None, gt=0)
    weight: Optional[Decimal] = Field(None, gt=0)

class BioMetricInDB(BioMetricBase):
    user_uuid: UUID
    bmi: Optional[Decimal] = None
    age: Optional[int] = None

    class Config:
        from_attributes = True

class BioMetricResponse(BioMetricInDB):
    pass
