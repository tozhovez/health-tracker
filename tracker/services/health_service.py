

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from sqlalchemy import text, func, desc, true
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Dict, Any, Optional, List, Tuple
from collections import Counter
from database.views import SystemAvgBiometricsDaily, SystemAvgPhysicalActivityDaily, SystemAvgSleepActivityDaily, SystemAvgBloodTestsDaily, UserBiometricsDaily, UserBloodTestsDaily, UserPhysicalActivityDaily, UserSleepActivityDaily
from schemas.health import TimeFrame, HealthMetricCategory, HealthScoreWeights
from pprint import pprint as print


class HealthService:
    @staticmethod
    async def get_health_metrics(db: AsyncSession, user_uuid: UUID, recorded: date = None):
       
        user_data = {}
        system_data = {}
        last_date = None
        for model in [UserBiometricsDaily, UserBloodTestsDaily, UserPhysicalActivityDaily, UserSleepActivityDaily]:
            result = await db.execute(
                select(model)
                .where(model.user_uuid == user_uuid)
                .where((model.bucket <= recorded) if recorded else true())
                .order_by(model.bucket.desc())
            )
            user_record = result.scalars().first()
            if user_record:
                if last_date:
                    last_date = max(last_date, user_record.bucket)
                else:
                    last_date = user_record.bucket
                user_data.update({column: getattr(user_record, column, None) for column in user_record.__table__.columns.keys() if  column not in ['user_uuid', 'bucket']})


        for model in [SystemAvgBiometricsDaily, SystemAvgPhysicalActivityDaily, SystemAvgSleepActivityDaily, SystemAvgBloodTestsDaily]:
            result = await db.execute(
                select(model)
                .where(model.bucket <= last_date.date())
                .order_by(model.bucket.desc())
                )
            system_records = result.scalars().first()
            if system_records:
                system_data.update({column: getattr(system_records, column, None) for column in system_records.__table__.columns.keys() if column != 'bucket'})
               
        return {"user_data": user_data,
                "system_data": system_data,
                "user_uuid": user_uuid,
                "last_date": last_date
                }


    @staticmethod
    def get_metrics(user_data: Dict[str, Any], system_data: Dict[str, Any])-> Dict[str, Any]:
        normalizer = lambda a, b: abs(b - a)
        if not user_data or  not system_data:
            return None
        deviations_data =  {
            "activity_duration": normalizer(system_data['avg_activity_duration'], user_data['user_sum_activity_duration']),
            "age": normalizer(system_data['avg_age'], user_data['user_age']),
            "calories_burned": normalizer(system_data['avg_calories_burned'],user_data['user_sum_calories_burned']),
            "sleep_duration": normalizer(system_data['avg_sleep_duration'], user_data['user_sum_sleep_duration']),
            "steps": normalizer(system_data['avg_steps']*1.00, user_data['user_avg_steps']*1.00),
            "bmi": normalizer(system_data['avg_bmi'], user_data['user_bmi']),
            "cholesterol": normalizer(system_data['avg_cholesterol'], user_data['user_cholesterol']),
            "cortisol": normalizer(system_data['avg_cortisol'], user_data['user_cortisol']),
            "glucose": normalizer(system_data['avg_glucose'], user_data['user_glucose']),
            "heart_rate_avg": normalizer(system_data['avg_heart_rate_avg'], user_data['user_avg_heart_rate_avg']),
            "melatonin": normalizer(system_data['avg_melatonin'], user_data['user_melatonin']),
            "sleep_quality": normalizer(system_data['avg_sleep_quality'],user_data['user_sleep_quality'])
        }
        return deviations_data
        
        
    @staticmethod
    async def get_health_score(db:AsyncSession, user_uuid: UUID, recorded: date = None):
        data = await HealthService.get_health_metrics(db, user_uuid, recorded)
        deviations = HealthService.get_metrics(data["user_data"], data["system_data"])
        data["normalizer"] = deviations
        data["deviation"] = {}
        for key, value in deviations.items():
            if key in HealthScoreWeights.WEIGHTS and key in deviations and value is not None:
                data["deviation"][key] = max(0, 100 -  HealthScoreWeights.WEIGHTS[key] * value*1.00)

        data["score"] = sum(data["deviation"].values()) / len( data["deviation"])
        
        return data


