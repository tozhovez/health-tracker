from sqlalchemy import Column, String, DateTime, Float, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID  
Base = declarative_base()

# System-level views
class SystemAvgBiometricsDaily(Base):
    __tablename__ = "system_avg_biometrics_daily"
    bucket = Column(DateTime, primary_key=True)
    avg_bmi = Column(Float)
    avg_age = Column(Float)
    total = Column(Integer)

class SystemAvgBiometricsMonthly(Base):
    __tablename__ = "system_avg_biometrics_monthly"
    bucket = Column(DateTime, primary_key=True)
    avg_bmi = Column(Float)
    avg_age = Column(Float)
    total = Column(Integer)

class SystemAvgBiometricsYearly(Base):
    __tablename__ = "system_avg_biometrics_yearly"
    bucket = Column(DateTime, primary_key=True)
    avg_bmi = Column(Float)
    avg_age = Column(Float)
    total = Column(Integer)

class SystemAvgPhysicalActivityDaily(Base):
    __tablename__ = "system_avg_physical_activity_daily"
    bucket = Column(DateTime, primary_key=True)
    avg_activity_duration = Column(Float)
    avg_steps = Column(Float)
    avg_calories_burned = Column(Float)
    avg_heart_rate_avg = Column(Float)
    total = Column(Integer)

class SystemAvgPhysicalActivityMonthly(Base):
    __tablename__ = "system_avg_physical_activity_monthly"
    bucket = Column(DateTime, primary_key=True)
    avg_activity_duration = Column(Float)
    avg_steps = Column(Float)
    avg_calories_burned = Column(Float)
    avg_heart_rate_avg = Column(Float)
    total = Column(Integer)

class SystemAvgPhysicalActivityYearly(Base):
    __tablename__ = "system_avg_physical_activity_yearly"
    bucket = Column(DateTime, primary_key=True)
    avg_activity_duration = Column(Float)
    avg_steps = Column(Float)
    avg_calories_burned = Column(Float)
    avg_heart_rate_avg = Column(Float)
    total = Column(Integer)

class SystemAvgSleepActivityDaily(Base):
    __tablename__ = "system_avg_sleep_activity_daily"
    bucket = Column(DateTime, primary_key=True)
    avg_sleep_duration = Column(Float)
    avg_sleep_quality = Column(Float)
    total = Column(Integer)

class SystemAvgSleepActivityMonthly(Base):
    __tablename__ = "system_avg_sleep_activity_monthly"
    bucket = Column(DateTime, primary_key=True)
    avg_sleep_duration = Column(Float)
    avg_sleep_quality = Column(Float)
    total = Column(Integer)

class SystemAvgSleepActivityYearly(Base):
    __tablename__ = "system_avg_sleep_activity_yearly"
    bucket = Column(DateTime, primary_key=True)
    avg_sleep_duration = Column(Float)
    avg_sleep_quality = Column(Float)
    total = Column(Integer)

class SystemAvgBloodTestsDaily(Base):
    __tablename__ = "system_avg_blood_tests_daily"
    bucket = Column(DateTime, primary_key=True)
    avg_glucose = Column(Float)
    avg_cholesterol = Column(Float)
    avg_cortisol = Column(Float)
    avg_melatonin = Column(Float)
    total = Column(Integer)

class SystemAvgBloodTestsMonthly(Base):
    __tablename__ = "system_avg_blood_tests_monthly"
    bucket = Column(DateTime, primary_key=True)
    avg_glucose = Column(Float)
    avg_cholesterol = Column(Float)
    avg_cortisol = Column(Float)
    avg_melatonin = Column(Float)
    total = Column(Integer)

class SystemAvgBloodTestsYearly(Base):
    __tablename__ = "system_avg_blood_tests_yearly"
    bucket = Column(DateTime, primary_key=True)
    avg_glucose = Column(Float)
    avg_cholesterol = Column(Float)
    avg_cortisol = Column(Float)
    avg_melatonin = Column(Float)
    total = Column(Integer)

# User-level views
class UserBiometricsDaily(Base):
    __tablename__ = "user_biometrics_daily"
    user_uuid = Column(UUID(as_uuid=True), primary_key=True, index=True)
    bucket = Column(DateTime, primary_key=True)
    user_bmi = Column(Float)
    user_age = Column(Integer)
    total = Column(Integer)

class UserBiometricsMonthly(Base):
    __tablename__ = "user_biometrics_monthly"
    user_uuid = Column(UUID(as_uuid=True), primary_key=True, index=True)
    bucket = Column(DateTime, primary_key=True)
    user_bmi = Column(Float)
    user_age = Column(Integer)
    total = Column(Integer)

class UserBiometricsYearly(Base):
    __tablename__ = "user_biometrics_yearly"
    user_uuid = Column(UUID(as_uuid=True), primary_key=True, index=True)
    bucket = Column(DateTime, primary_key=True)
    user_bmi = Column(Float)
    user_age = Column(Integer)
    total = Column(Integer) 

class UserBloodTestsDaily(Base):
    __tablename__ = "user_blood_tests_daily"
    user_uuid = Column(UUID(as_uuid=True), primary_key=True, index=True)
    bucket = Column(DateTime, primary_key=True)
    user_glucose = Column(Float)
    user_cholesterol = Column(Float)
    user_cortisol = Column(Float)
    user_melatonin = Column(Float)
    user_avg_glucose = Column(Float)
    user_avg_cholesterol = Column(Float)
    user_avg_cortisol = Column(Float)
    user_avg_melatonin = Column(Float)
    total = Column(Integer)

class UserBloodTestsMonthly(Base):
    __tablename__ = "user_blood_tests_monthly"
    user_uuid = Column(UUID(as_uuid=True), primary_key=True, index=True)
    bucket = Column(DateTime, primary_key=True)
    user_glucose = Column(Float)
    user_cholesterol = Column(Float)
    user_cortisol = Column(Float)
    user_melatonin = Column(Float)
    user_avg_glucose = Column(Float)
    user_avg_cholesterol = Column(Float)
    user_avg_cortisol = Column(Float)
    user_avg_melatonin = Column(Float)
    total = Column(Integer)

class UserBloodTestsYearly(Base):
    __tablename__ = "user_blood_tests_yearly"
    user_uuid = Column(UUID(as_uuid=True), primary_key=True, index=True)
    bucket = Column(DateTime, primary_key=True)
    user_glucose = Column(Float)
    user_cholesterol = Column(Float)
    user_cortisol = Column(Float)
    user_melatonin = Column(Float)
    user_avg_glucose = Column(Float)
    user_avg_cholesterol = Column(Float)
    user_avg_cortisol = Column(Float)
    user_avg_melatonin = Column(Float)
    total = Column(Integer)

class UserPhysicalActivityDaily(Base):
    __tablename__ = "user_physical_activity_daily"
    user_uuid = Column(UUID(as_uuid=True), primary_key=True, index=True)
    bucket = Column(DateTime, primary_key=True)
    user_sum_activity_duration = Column(Float)
    user_sum_steps = Column(Integer)
    user_sum_calories_burned = Column(Integer)
    user_avg_activity_duration = Column(Float)
    user_avg_steps = Column(Float)
    user_avg_calories_burned = Column(Float)
    user_avg_heart_rate_avg = Column(Float)
    total = Column(Integer)

class UserPhysicalActivityMonthly(Base):
    __tablename__ = "user_physical_activity_monthly"
    user_uuid = Column(UUID(as_uuid=True), primary_key=True, index=True)
    bucket = Column(DateTime, primary_key=True)
    user_sum_activity_duration = Column(Float)
    user_sum_steps = Column(Integer)
    user_sum_calories_burned = Column(Integer)
    user_avg_activity_duration = Column(Float)
    user_avg_steps = Column(Float)
    user_avg_calories_burned = Column(Float)
    user_avg_heart_rate_avg = Column(Float)
    total = Column(Integer)

class UserPhysicalActivityYearly(Base):
    __tablename__ = "user_physical_activity_yearly"
    user_uuid = Column(UUID(as_uuid=True), primary_key=True, index=True)
    bucket = Column(DateTime, primary_key=True)
    user_sum_activity_duration = Column(Float)
    user_sum_steps = Column(Integer)
    user_sum_calories_burned = Column(Integer)
    user_avg_activity_duration = Column(Float)
    user_avg_steps = Column(Float)
    user_avg_calories_burned = Column(Float)
    user_avg_heart_rate_avg = Column(Float)
    total = Column(Integer)

class UserSleepActivityDaily(Base):
    __tablename__ = "user_sleep_activity_daily"
    user_uuid = Column(UUID(as_uuid=True), primary_key=True, index=True)
    bucket = Column(DateTime, primary_key=True)
    user_sum_sleep_duration = Column(Float)
    user_avg_sleep_duration = Column(Float)
    user_sleep_quality = Column(Float)
    total = Column(Integer)

class UserSleepActivityMonthly(Base):
    __tablename__ = "user_sleep_activity_monthly"
    user_uuid = Column(UUID(as_uuid=True), primary_key=True, index=True)
    bucket = Column(DateTime, primary_key=True)
    user_sum_sleep_duration = Column(Float)
    user_avg_sleep_duration = Column(Float)
    user_sleep_quality = Column(Float)
    total = Column(Integer)

class UserSleepActivityYearly(Base):
    __tablename__ = "user_sleep_activity_yearly"
    user_uuid = Column(UUID(as_uuid=True), primary_key=True, index=True)
    bucket = Column(DateTime, primary_key=True)
    user_sum_sleep_duration = Column(Float)
    user_avg_sleep_duration = Column(Float)
    user_sleep_quality = Column(Float)
    total = Column(Integer)