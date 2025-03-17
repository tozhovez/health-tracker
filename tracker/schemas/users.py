from typing import Optional
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field, validator

class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(..., max_length=50)
    phone_number: str = Field(..., min_length=5, max_length=20)
    address: Optional[str] = Field(None, max_length=100)
    birthday: date
    gender: str = Field(..., min_length=1, max_length=1)

    @validator('gender')
    def validate_gender(cls, v):
        if v not in ['f', 'm']:
            raise ValueError('Gender must be "f" or "m"')
        return v

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=50)
    phone_number: Optional[str] = Field(None, min_length=5, max_length=20)
    address: Optional[str] = Field(None, max_length=100)
    birthday: Optional[date] = None
    gender: Optional[str] = Field(None, min_length=1, max_length=1)

    @validator('gender')
    def validate_gender(cls, v):
        if v is not None and v not in ['f', 'm']:
            raise ValueError('Gender must be "f" or "m"')
        return v

class UserInDB(UserBase):
    user_uuid: UUID
    created_date: datetime
    updated_date: datetime

    class Config:
        from_attributes = True

class UserResponse(UserInDB):
    pass
