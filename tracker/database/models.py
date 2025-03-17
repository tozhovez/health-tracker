import uuid
from sqlalchemy import Column, String, Integer, Float, ForeignKey, UniqueConstraint, CheckConstraint, Date, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID, INTERVAL, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
# Create declarative base for models
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone_number = Column(String(20), nullable=False, unique=True)
    address = Column(String(100))
    birthday = Column(Date, nullable=False)
    gender = Column(String(1), nullable=False, default='f')
    created_date = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_date = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    __table_args__ = (
        UniqueConstraint('email', 'phone_number', name='users_email_phone_number'),
        CheckConstraint("gender IN ('f', 'm')", name='check_gender'),
    )

class PhysicalActivity(Base):
    __tablename__ = "physical_activity"
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.user_uuid', ondelete='CASCADE'), nullable=False, primary_key=True)
    start_time = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, primary_key=True)
    activity_duration = Column(Float, nullable=False, default=0.00)
    steps = Column(Integer, default=0)
    calories_burned = Column(Integer)
    heart_rate_avg = Column(Integer)
    created_by = Column(String(50), nullable=False, default='user')
    created_date = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_date = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    __table_args__ = (
     
        CheckConstraint("steps >= 0", name='check_steps'),
        CheckConstraint("created_by IN ('user', 'device', 'medical')", name='check_physical_activity_created_by'),
    )

class SleepActivity(Base):
    __tablename__ = "sleep_activity"
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.user_uuid', ondelete='CASCADE'), nullable=False, primary_key=True)
    start_time = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, primary_key=True)
    sleep_duration = Column(Float, nullable=False, default=0.00 )
    sleep_quality = Column(Integer, default=0)
    created_by = Column(String(50), nullable=False, default='user')
    created_date = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_date = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    __table_args__ = (
       
        CheckConstraint("created_by IN ('user', 'device', 'medical')", name='check_sleep_activity_created_by'),
        CheckConstraint("sleep_quality BETWEEN 1 AND 10", name='check_sleep_quality'),
    )

class BloodTest(Base):
    __tablename__ = "blood_tests"
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.user_uuid', ondelete='CASCADE'), nullable=False, primary_key=True)
    test_date = Column(TIMESTAMP(timezone=True), nullable=False, primary_key=True)
    glucose_level = Column(Float)
    cholesterol_level = Column(Float)
    cortisol_level = Column(Float)
    melatonin_level = Column(Float)
    created_by = Column(String(50), nullable=False, default='user')
    created_date = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_date = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    __table_args__ = (
        CheckConstraint("created_by IN ('user', 'device', 'medical')", name='check_blood_tests_created_by'),
    )

class BioMetric(Base):
    __tablename__ = "biometrics"
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.user_uuid', ondelete='CASCADE'), nullable=False, primary_key=True)
    height = Column(Numeric(5, 2))
    weight = Column(Numeric(5, 2))
    bmi = Column(Numeric(5, 2))
    age = Column(Integer)
    recorded = Column(TIMESTAMP(timezone=True), server_default=func.now(), primary_key=True)
    __table_args__ = (
        UniqueConstraint('user_uuid', 'recorded', name='bio_metrics_user_uuid_recorded_key'),
    )

