from enum import Enum

# Enhanced Schema Definitions
class TimeFrame(str, Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"

class HealthMetricCategory(str, Enum):
    BIOMETRICS = "biometrics"
    BLOOD_TESTS = "blood_tests"
    PHYSICAL_ACTIVITY = "physical_activity"
    SLEEP = "sleep"
    ALL = "all"

class HealthScoreWeights:
    # Default weights for different health metrics
    BIOMETRIC_WEIGHT = 0.20
    BLOOD_TEST_WEIGHT = 0.10
    PHYSICAL_ACTIVITY_WEIGHT = 0.35
    SLEEP_WEIGHT = 0.35
    # Sub-weights within categories
    WEIGHTS = {
        "bmi": 0.10,
        "age": 0.05,
        "melatonin": 0.05,
        "glucose": 0.10,
        "cholesterol": 0.10,
        "cortisol": 0.05,
        "calories_burned": 0.05,

        "activity_duration": 0.10,

        "steps": 0.10,

        "heart_rate_avg": 0.10,
        "sleep_duration": 0.10,
     
        "sleep_quality": 0.10
        }

    BIOMETRIC_WEIGHT = {
        "bmi": 0.90,
        "age": 0.10,
    }

    BLOOD_TEST_WEIGHTS = {
        "glucose": 0.35,
        "cholesterol": 0.35,
        "cortisol": 0.10,
        "melatonin": 0.20
    }
    PHYSICAL_ACTIVITY_WEIGHTS = {
        "activity_duration": 0.35,
        "steps": 0.30,
        "calories_burned": 0.15,
        "heart_rate_avg": 0.20
    }
    SLEEP_WEIGHTS = {
        "sleep_duration": 0.60,
        "sleep_quality": 0.40
    }
    
    
