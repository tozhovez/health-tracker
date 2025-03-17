CREATE TABLE IF NOT EXISTS users (
    user_uuid UUID DEFAULT gen_random_uuid(),
    first_name CHARACTER VARYING(50) NOT NULL,
    last_name CHARACTER VARYING(50) NOT NULL,
    email CHARACTER VARYING(50) NOT NULL,
    phone_number CHARACTER VARYING(20) NOT NULL,
    address CHARACTER VARYING(100),
    birthday  DATE NOT NULL,
    gender CHARACTER VARYING(1) NOT NULL DEFAULT 'f',
    created_date TIMESTAMPTZ DEFAULT now(),
    updated_date TIMESTAMPTZ DEFAULT now(),
    CONSTRAINT users_email_phone_number UNIQUE (email, phone_number),
    CONSTRAINT users_pkey PRIMARY KEY (user_uuid),
    CONSTRAINT check_gender CHECK (gender IN ('f', 'm'))
);

CREATE TABLE IF NOT EXISTS physical_activity (
    user_uuid UUID NOT NULL,
    start_time TIMESTAMPTZ NOT NULL DEFAULT now(),
    activity_duration DOUBLE PRECISION NOT NULL DEFAULT 0.00,
    steps INT DEFAULT 0,
    calories_burned INT,
    heart_rate_avg INT ,
    created_by VARCHAR(50) NOT NULL DEFAULT 'user',
    created_date TIMESTAMPTZ DEFAULT now(),
    updated_date TIMESTAMPTZ DEFAULT now(),
    CONSTRAINT physical_activity_user_uuid_start_time_key PRIMARY KEY (user_uuid, start_time),
    CONSTRAINT fk_physical_activity_user FOREIGN KEY (user_uuid) REFERENCES users(user_uuid) ON DELETE CASCADE,
    CONSTRAINT check_steps CHECK (steps >= 0),
    CONSTRAINT check_physical_activity_created_by CHECK (created_by IN ('user', 'device', 'medical'))
);


CREATE TABLE IF NOT EXISTS sleep_activity (
    user_uuid UUID NOT NULL,
    start_time TIMESTAMPTZ NOT NULL DEFAULT now(),
    sleep_duration DOUBLE PRECISION NOT NULL DEFAULT 0.00,
    sleep_quality INTEGER DEFAULT 0,
    created_by VARCHAR(50) NOT NULL DEFAULT 'user',
    created_date TIMESTAMPTZ DEFAULT now(),
    updated_date TIMESTAMPTZ DEFAULT now(),
    CONSTRAINT sleep_activity_user_uuid_start_time_key PRIMARY KEY (user_uuid, start_time),
    CONSTRAINT fk_user FOREIGN KEY (user_uuid) REFERENCES users(user_uuid) ON DELETE CASCADE,
    CONSTRAINT check_sleep_activity_created_by CHECK (created_by IN ('user', 'device', 'medical')),
    CONSTRAINT check_sleep_quality CHECK (sleep_quality BETWEEN 1 AND 10)
);


CREATE TABLE IF NOT EXISTS blood_tests (
    user_uuid UUID NOT NULL,
    test_date TIMESTAMPTZ NOT NULL,
    glucose_level DOUBLE PRECISION,
    cholesterol_level DOUBLE PRECISION,
    cortisol_level DOUBLE PRECISION,
    melatonin_level DOUBLE PRECISION,
    created_by VARCHAR(50) NOT NULL DEFAULT 'user',
    created_date TIMESTAMPTZ DEFAULT now(),
    updated_date TIMESTAMPTZ DEFAULT now(),
    CONSTRAINT check_blood_tests_created_by CHECK (created_by IN ('user', 'device', 'medical')),
    CONSTRAINT blood_tests_user_uuid_test_date_key PRIMARY KEY (user_uuid, test_date),
    CONSTRAINT fk_blood_tests_user FOREIGN KEY (user_uuid) REFERENCES users(user_uuid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS biometrics (
    user_uuid UUID NOT NULL,
    height NUMERIC(5,2),
    weight NUMERIC(5,2),
    bmi NUMERIC(5,2), --  weight/(height*height)
    age INT,
    recorded TIMESTAMPTZ DEFAULT now(),
    CONSTRAINT fk_biometrics_user FOREIGN KEY (user_uuid) REFERENCES users(user_uuid) ON DELETE CASCADE,
    CONSTRAINT biometrics_user_uuid_recorded_key PRIMARY KEY (user_uuid, recorded)
);


CREATE OR REPLACE FUNCTION set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_date = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_timestamp_users
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION set_timestamp();

CREATE TRIGGER update_timestamp_physical_activity
BEFORE UPDATE ON physical_activity
FOR EACH ROW
EXECUTE FUNCTION set_timestamp();

CREATE TRIGGER update_timestamp_sleep_activity
BEFORE UPDATE ON sleep_activity
FOR EACH ROW
EXECUTE FUNCTION set_timestamp();

CREATE TRIGGER update_timestamp_blood_tests
BEFORE UPDATE ON blood_tests
FOR EACH ROW
EXECUTE FUNCTION set_timestamp();

CREATE OR REPLACE FUNCTION set_user_age()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE biometrics
    SET age = EXTRACT(YEAR FROM AGE(NEW.recorded, u.birthday))::INT
    FROM users u
    WHERE biometrics.user_uuid = u.user_uuid
    AND biometrics.user_uuid = NEW.user_uuid
    AND biometrics.recorded = NEW.recorded;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER insert_user_age_biometrics
AFTER INSERT ON biometrics
FOR EACH ROW
EXECUTE FUNCTION set_user_age();

CREATE OR REPLACE FUNCTION set_user_bmi()
RETURNS TRIGGER AS $$
BEGIN
    IF (NEW.weight IS NOT NULL AND NEW.height IS NOT NULL AND NEW.bmi IS NULL) OR
       (OLD.weight IS DISTINCT FROM NEW.weight OR OLD.height IS DISTINCT FROM NEW.height) THEN
        NEW.bmi = (10000.00 * NEW.weight) / (NEW.height * NEW.height);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_user_bmi_biometrics
BEFORE INSERT OR UPDATE ON biometrics
FOR EACH ROW
EXECUTE FUNCTION set_user_bmi();

SELECT create_hypertable('physical_activity', by_range('start_time'), if_not_exists => TRUE);
SELECT create_hypertable('sleep_activity', by_range('start_time'), if_not_exists => TRUE);
SELECT create_hypertable('blood_tests', by_range('test_date'), if_not_exists => TRUE);
SELECT create_hypertable('biometrics', by_range('recorded'), if_not_exists => TRUE);




