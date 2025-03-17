"""Script generate dummy data for database with more realistic values"""

import uuid
import random
from datetime import datetime, timedelta
import faker

NUM_BLOOD_TESTS = 10
NUM_SLEEP_RECORDS = 100  # максимальное число записей сна на пользователя
NUM_ACTIVITIES = 100
NUM_USERS = 10
NUM_BIOMETRICS = 25

CREATED_BY_OPTIONS = ['user', 'device', 'medical']
fake = faker.Faker()


def generate_users(num_users=1000):
    users = []
    user_uuids = {}
    for _ in range(num_users):
        user_uuid = str(uuid.uuid4())
        fname = fake.first_name()
        lname = fake.last_name()
        email = fake.unique.email()
        phone = f"{fake.country_calling_code()}-{fake.unique.msisdn()}"
        phone = str(phone[0:min(15, len(phone))])
        address = fake.address().replace("'", "''")
        # Изменили maximum_age с 90 на 100, чтобы возраст был в диапазоне 18-100 лет
        birthday_date = fake.date_of_birth(minimum_age=18, maximum_age=100)
        birthday = birthday_date.strftime('%Y-%m-%d')
        gender = random.choice(['m', 'f'])
        created = fake.date_time_between(start_date='-1y', end_date='-11m')
        updated = created.strftime('%Y-%m-%d %H:%M:%S')
        users.append(
            f"('{user_uuid}', '{fname}', '{lname}', '{email}', '{phone}', "
            f"'{address}', '{birthday}', '{gender}', '{created.strftime('%Y-%m-%d %H:%M:%S')}', '{updated}')"
        )
        # Сохраняем базовую информацию для дальнейших вычислений
        user_uuids[user_uuid] = {
            'created': created,
            'birthday': birthday_date,
            'gender': gender
        }
    return user_uuids, ",\n".join(users)


def generate_biometrics(user_uuids, num_biometrics=10):
    biometrics = []
    for user_uuid in user_uuids:
        # Генерируем базовые биометрические данные для пользователя
        height = round(random.uniform(1.2, 2.0), 2)  # рост в метрах
        base_bmi = round(random.uniform(18.5, 30), 2)  # базовый BMI
        weight = round(base_bmi * (height ** 2), 2)     # вес в кг
        # Сохраняем базовые биометрики для дальнейших вычислений
        user_uuids[user_uuid]['biometric'] = {
            'height': height,
            'weight': weight,
            'bmi': base_bmi
        }
        for i in range(num_biometrics):
            recorded = fake.date_time_between(start_date=user_uuids[user_uuid]['created'], end_date='-1d')
            # Небольшое колебание веса
            weight_variation = round(random.uniform(-1, 1), 2)
            current_weight = round(weight + weight_variation, 2)
            current_bmi = round(current_weight / (height ** 2), 2)
            biometrics.append(
                f"('{user_uuid}', {int(height * 100)}, {current_weight}, {current_bmi}, '{recorded.strftime('%Y-%m-%d %H:%M:%S')}')"
            )
            # Обновляем последние биометрики, если запись новее
            if 'latest_recorded' not in user_uuids[user_uuid] or recorded > user_uuids[user_uuid]['latest_recorded']:
                user_uuids[user_uuid]['latest_recorded'] = recorded
                user_uuids[user_uuid]['biometric'] = {
                    'height': height,
                    'weight': current_weight,
                    'bmi': current_bmi
                }
    return ",\n".join(biometrics)


def generate_physical_activity(user_uuids, num_activities=100):
    activities = []
    for user_uuid, data in user_uuids.items():
        # Вычисляем возраст пользователя
        today = datetime.now()
        age = today.year - data['birthday'].year
        gender = data['gender']
        biometric = data.get('biometric', {'weight': 70})
        weight = biometric.get('weight', 70)
        # Определяем базовую скорость шагов (шагов в минуту)
        step_rate = 100 if gender == 'm' else 90
        if age > 50:
            step_rate = int(step_rate * 0.9)  # снижение темпа для пожилых
        for i in range(num_activities):
            # Генерируем время начала активности в дневное время (07:00-21:00)
            base_date = fake.date_time_between(start_date=data['created'], end_date='-1d')
            start_hour = random.randint(7, 21)
            start_minute = random.randint(0, 59)
            start_time = base_date.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)
            # Длительность активности от 10 до 120 минут
            duration_minutes = random.randint(10, 120)
            duration = timedelta(minutes=duration_minutes)
            end_time = start_time + duration
            # Шаги пропорциональны длительности и базовой скорости, с небольшим шумом
            steps = int(duration_minutes * step_rate * random.uniform(0.9, 1.1))
            # Потеря калорий – упрощённая формула: (время в часах) * вес * 3.5 с шумом
            duration_hours = duration_minutes / 60
            calories_burned = int(duration_hours * weight * 3.5 * random.uniform(0.9, 1.1))
            # Средний пульс – приблизительно 60% от максимального (220 - возраст)
            heart_rate_avg = int(0.6 * (220 - age) * random.uniform(0.9, 1.1))
            created_by = random.choice(CREATED_BY_OPTIONS)
            created = end_time.strftime('%Y-%m-%d %H:%M:%S')
            updated = created
            duration_hours = duration.total_seconds() / 3600
            activities.append(
                f"('{user_uuid}', {calories_burned}, {heart_rate_avg}, {steps}, '{duration_hours:.2f}', "
                f"'{start_time.strftime('%Y-%m-%d %H:%M:%S')}', '{created_by}', '{created}', '{updated}')"
            )
    return ",\n".join(activities)


def generate_sleep_activity(user_uuids, num_records=100):
    sleep_records = []
    for user_uuid, data in user_uuids.items():
        # Генерируем записи сна по уникальным датам без пересечений
        start_date = data['created'].date()
        end_date = (datetime.now() - timedelta(days=1)).date()
        # Получаем список всех дней между датой создания и вчерашним днём
        available_days = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
        # Выбираем случайное подмножество дней (максимум num_records записей)
        chosen_days = random.sample(available_days, min(num_records, len(available_days)))
        for day in chosen_days:
            # Генерируем время начала сна в вечерние часы (от 21:00 до 23:00)
            hour = random.randint(21, 23)
            minute = random.randint(0, 59)
            sleep_start = datetime.combine(day, datetime.min.time()) + timedelta(hours=hour, minutes=minute)
            # Длительность сна от 5 до 9 часов
            sleep_duration_minutes = random.randint(300, 540)
            sleep_duration = timedelta(minutes=sleep_duration_minutes)
            end_time = sleep_start + sleep_duration
            # Перевод в часы
            sleep_duration_hours = sleep_duration.total_seconds() / 3600
            sleep_quality = random.randint(1, 10)
            created_by = random.choice(CREATED_BY_OPTIONS)
            created = end_time.strftime('%Y-%m-%d %H:%M:%S')
            updated = created
            sleep_records.append(
                f"('{user_uuid}', '{sleep_duration_hours:.2f}', {sleep_quality}, "
                f"'{sleep_start.strftime('%Y-%m-%d %H:%M:%S')}', '{created_by}', '{created}', '{updated}')"
            )
    return ",\n".join(sleep_records)


def generate_blood_tests(user_uuids, num_tests=10):
    tests = []
    for user_uuid, data in user_uuids.items():
        biometric = data.get('biometric', {'weight': 70})
        weight = biometric.get('weight', 70)
        for _ in range(num_tests):
            date = fake.date_time_between(start_date=data['created'], end_date='-1d')
            # Диапазоны скорректированы в зависимости от базового веса
            glucose = round(random.uniform(70 + (weight - 70) * 0.5, 140 + (weight - 70) * 0.5), 2)
            cholesterol = round(random.uniform(150 + (weight - 70) * 0.3, 240 + (weight - 70) * 0.3), 2)
            cortisol = round(random.uniform(4, 30), 2)
            melatonin = round(random.uniform(5, 160), 2)
            created_by = random.choice(CREATED_BY_OPTIONS)
            created = (min(date + timedelta(hours=random.randint(0, 3), minutes=random.randint(0, 59)), datetime.now())
                       ).strftime('%Y-%m-%d %H:%M:%S')
            updated = created
            tests.append(
                f"('{user_uuid}', '{date.strftime('%Y-%m-%d %H:%M:%S')}', {glucose}, {cholesterol}, "
                f"{cortisol}, {melatonin}, '{created_by}', '{created}', '{updated}')"
            )
    return ",\n".join(tests)


# Генерация данных
users_uuids, users_data = generate_users(NUM_USERS)
biometrics_data = generate_biometrics(users_uuids, NUM_BIOMETRICS)
activities_data = generate_physical_activity(users_uuids, NUM_ACTIVITIES)
sleep_data = generate_sleep_activity(users_uuids, NUM_SLEEP_RECORDS)
blood_tests_data = generate_blood_tests(users_uuids, NUM_BLOOD_TESTS)

sql_statements_users = """
INSERT INTO users (user_uuid, first_name, last_name, email, phone_number, address, birthday, gender, created_date, updated_date) VALUES
"""
sql_statements_biometrics = """
INSERT INTO biometrics (user_uuid, height, weight, bmi, recorded) VALUES
"""
sql_statements_physical_activity = """
INSERT INTO physical_activity (user_uuid, calories_burned, heart_rate_avg, steps, activity_duration, start_time, created_by, created_date, updated_date) VALUES
"""
sql_statements_sleep_activity = """
INSERT INTO sleep_activity (user_uuid, sleep_duration, sleep_quality, start_time, created_by, created_date, updated_date) VALUES
"""
sql_statements_blood_tests = """
INSERT INTO blood_tests (user_uuid, test_date, glucose_level, cholesterol_level, cortisol_level, melatonin_level, created_by, created_date, updated_date) VALUES
"""

# Сохранение в файл
with open("dummy_data.sql", "w", encoding="utf-8") as f:
    f.write(
        f"{sql_statements_users}\n{users_data};" +
        f"\n{sql_statements_biometrics}\n{biometrics_data} ON CONFLICT (user_uuid, recorded)DO NOTHING;" +
        f"\n{sql_statements_physical_activity}\n{activities_data} ON CONFLICT (user_uuid, start_time)DO NOTHING;" +
        f"\n{sql_statements_sleep_activity}\n{sleep_data} ON CONFLICT (user_uuid, start_time)DO NOTHING;" +
        f"\n{sql_statements_blood_tests}\n{blood_tests_data} ON CONFLICT (user_uuid, test_date)DO NOTHING;"
    )

print("dummy_data.sql created!")
