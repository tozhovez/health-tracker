
DROP  MATERIALIZED VIEW IF EXISTS system_avg_biometrics_daily;

CREATE MATERIALIZED VIEW system_avg_biometrics_daily
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 day', recorded)  AS bucket,
    AVG(bmi) AS avg_bmi,
    AVG(age) AS avg_age,
    COUNT(*) AS total
FROM biometrics
GROUP BY bucket;


DROP  MATERIALIZED VIEW IF EXISTS system_avg_biometrics_monthly;

CREATE MATERIALIZED VIEW system_avg_biometrics_monthly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 month', recorded)  AS bucket,
    AVG(bmi) AS avg_bmi,
    AVG(age) AS avg_age,
    COUNT(*) AS total
FROM biometrics
GROUP BY bucket;

DROP  MATERIALIZED VIEW IF EXISTS system_avg_biometrics_yearly;

CREATE MATERIALIZED VIEW system_avg_biometrics_yearly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 year', recorded)  AS bucket,
    AVG(bmi) AS avg_bmi,
    AVG(age) AS avg_age,
    COUNT(*) AS total
FROM biometrics
GROUP BY bucket;

SELECT add_continuous_aggregate_policy('system_avg_biometrics_yearly',
    start_offset => NULL,
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 day'
);

SELECT add_continuous_aggregate_policy('system_avg_biometrics_monthly',
    start_offset => INTERVAL '1 year',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 day'
);

SELECT add_continuous_aggregate_policy('system_avg_biometrics_daily',
    start_offset => INTERVAL '7 day',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 minute'
);

DROP  MATERIALIZED VIEW IF EXISTS system_avg_physical_activity_daily;

CREATE MATERIALIZED VIEW system_avg_physical_activity_daily
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 day', start_time) AS bucket,
    AVG(activity_duration) as avg_activity_duration,
    AVG(steps) AS avg_steps,
    AVG(calories_burned) AS avg_calories_burned,
    AVG(heart_rate_avg) AS avg_heart_rate_avg,
    COUNT(*) AS total
FROM physical_activity
GROUP BY bucket
ORDER BY bucket DESC;


SELECT add_continuous_aggregate_policy('system_avg_physical_activity_daily',
    start_offset => INTERVAL '1 year',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 day'
);

DROP  MATERIALIZED VIEW IF EXISTS system_avg_physical_activity_monthly;

CREATE MATERIALIZED VIEW system_avg_physical_activity_monthly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 month', start_time) AS bucket,
    AVG(activity_duration) as avg_activity_duration,
    AVG(steps) AS avg_steps,
    AVG(calories_burned) AS avg_calories_burned,
    AVG(heart_rate_avg) AS avg_heart_rate_avg,
    COUNT(*) AS total
FROM physical_activity
GROUP BY bucket
ORDER BY bucket DESC;


SELECT add_continuous_aggregate_policy('system_avg_physical_activity_monthly',
    start_offset => NULL,
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 day'
);


DROP  MATERIALIZED VIEW IF EXISTS system_avg_physical_activity_yearly;

CREATE MATERIALIZED VIEW system_avg_physical_activity_yearly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 year', start_time) AS bucket,
    AVG(activity_duration) as avg_activity_duration,
    AVG(steps) AS avg_steps,
    AVG(calories_burned) AS avg_calories_burned,
    AVG(heart_rate_avg) AS avg_heart_rate_avg,
    COUNT(*) AS total
FROM physical_activity
GROUP BY bucket
ORDER BY bucket DESC;


SELECT add_continuous_aggregate_policy('system_avg_physical_activity_yearly',
    start_offset => NULL,
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 day'
);

DROP  MATERIALIZED VIEW IF EXISTS system_avg_sleep_activity_daily;

CREATE MATERIALIZED VIEW system_avg_sleep_activity_daily
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 day', start_time) AS bucket,
    AVG(sleep_duration) AS avg_sleep_duration,
    AVG(sleep_quality) AS avg_sleep_quality,
    COUNT(*) AS total
    
FROM sleep_activity
GROUP BY bucket
ORDER BY bucket DESC;

SELECT add_continuous_aggregate_policy('system_avg_sleep_activity_daily',
    start_offset => INTERVAL '7 day',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 minute'
);
DROP  MATERIALIZED VIEW IF EXISTS system_avg_sleep_activity_monthly;

CREATE MATERIALIZED VIEW system_avg_sleep_activity_monthly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 month', start_time) AS bucket,
    AVG(sleep_duration) AS avg_sleep_duration,
    AVG(sleep_quality) AS avg_sleep_quality,
    COUNT(*) AS total

FROM sleep_activity
GROUP BY bucket
ORDER BY bucket DESC;

SELECT add_continuous_aggregate_policy('system_avg_sleep_activity_monthly',
    start_offset => INTERVAL '1year',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 day'
);

DROP  MATERIALIZED VIEW IF EXISTS system_avg_sleep_activity_yearly;

CREATE MATERIALIZED VIEW system_avg_sleep_activity_yearly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 year', start_time) AS bucket,
    AVG(sleep_duration) AS avg_sleep_duration,
    AVG(sleep_quality) AS avg_sleep_quality,
    COUNT(*) AS total
    
FROM sleep_activity
GROUP BY bucket
ORDER BY bucket DESC;

SELECT add_continuous_aggregate_policy('system_avg_sleep_activity_yearly',
    start_offset => NULL,
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 day'
);

DROP  MATERIALIZED VIEW IF EXISTS system_avg_blood_tests_daily;


CREATE MATERIALIZED VIEW system_avg_blood_tests_daily
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 day', test_date) AS bucket,
    AVG(glucose_level) AS avg_glucose,
    AVG(cholesterol_level) AS avg_cholesterol,
    AVG(cortisol_level) AS avg_cortisol,
    AVG(melatonin_level) AS avg_melatonin,
    COUNT(*) AS total
FROM blood_tests
GROUP BY bucket
ORDER BY bucket DESC
;

SELECT add_continuous_aggregate_policy('system_avg_blood_tests_daily',
    start_offset => INTERVAL '7 day',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 minute'
);


DROP  MATERIALIZED VIEW IF EXISTS system_avg_blood_tests_monthly;


CREATE MATERIALIZED VIEW system_avg_blood_tests_monthly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 month', test_date) AS bucket,
    AVG(glucose_level) AS avg_glucose,
    AVG(cholesterol_level) AS avg_cholesterol,
    AVG(cortisol_level) AS avg_cortisol,
    AVG(melatonin_level) AS avg_melatonin,
    COUNT(*) AS total
FROM blood_tests
GROUP BY bucket
ORDER BY bucket DESC
;

SELECT add_continuous_aggregate_policy('system_avg_blood_tests_monthly',
    start_offset => INTERVAL '1 year',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 day'
);

DROP  MATERIALIZED VIEW IF EXISTS system_avg_blood_tests_yearly;


CREATE MATERIALIZED VIEW system_avg_blood_tests_yearly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 year', test_date) AS bucket,
    AVG(glucose_level) AS avg_glucose,
    AVG(cholesterol_level) AS avg_cholesterol,
    AVG(cortisol_level) AS avg_cortisol,
    AVG(melatonin_level) AS avg_melatonin,
    COUNT(*) AS total
FROM blood_tests
GROUP BY bucket
ORDER BY bucket DESC
;

SELECT add_continuous_aggregate_policy('system_avg_blood_tests_yearly',
    start_offset => NULL,
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 day'
);



DROP  MATERIALIZED VIEW IF EXISTS user_physical_activity_daily;

CREATE MATERIALIZED VIEW user_physical_activity_daily
WITH (timescaledb.continuous) AS
SELECT
    user_uuid,
    time_bucket('1 day', start_time) AS bucket,
    SUM(activity_duration) AS user_sum_activity_duration,
    SUM(steps) AS user_sum_steps,
    SUM(calories_burned) AS user_sum_calories_burned,
    AVG(activity_duration) AS user_avg_activity_duration,
    AVG(steps) AS user_avg_steps,
    AVG(calories_burned) AS user_avg_calories_burned,
    ROUND(AVG(heart_rate_avg)::numeric, 2) AS user_avg_heart_rate_avg,
    COUNT(*) AS total
FROM physical_activity
GROUP BY user_uuid, bucket
ORDER BY bucket DESC;


SELECT add_continuous_aggregate_policy('user_physical_activity_daily',
    start_offset => INTERVAL '1 month',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 day'
);

DROP  MATERIALIZED VIEW IF EXISTS user_physical_activity_monthly;

CREATE MATERIALIZED VIEW user_physical_activity_monthly
WITH (timescaledb.continuous) AS
SELECT
    user_uuid,
    time_bucket('1 month', start_time) AS bucket,
    SUM(activity_duration) AS user_sum_activity_duration,
    SUM(steps) AS user_sum_steps,
    SUM(calories_burned) AS user_sum_calories_burned,
    AVG(activity_duration) AS user_avg_activity_duration,
    AVG(steps) AS user_avg_steps,
    AVG(calories_burned) AS user_avg_calories_burned,
    ROUND(AVG(heart_rate_avg)::numeric, 2) AS user_avg_heart_rate_avg,
    COUNT(*) AS total
FROM physical_activity
GROUP BY user_uuid, bucket
ORDER BY bucket DESC;


SELECT add_continuous_aggregate_policy('user_physical_activity_monthly',
    start_offset => INTERVAL '1 year',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 day'
);

DROP  MATERIALIZED VIEW IF EXISTS user_physical_activity_yearly;

CREATE MATERIALIZED VIEW user_physical_activity_yearly
WITH (timescaledb.continuous) AS
SELECT
    user_uuid,
    time_bucket('1 year', start_time) AS bucket,
    SUM(activity_duration) AS user_sum_activity_duration,
    SUM(steps) AS user_sum_steps,
    SUM(calories_burned) AS user_sum_calories_burned,
    AVG(activity_duration) AS user_avg_activity_duration,
    AVG(steps) AS user_avg_steps,
    AVG(calories_burned) AS user_avg_calories_burned,
    ROUND(AVG(heart_rate_avg)::numeric, 2) AS user_avg_heart_rate_avg,
    COUNT(*) AS total
FROM physical_activity
GROUP BY user_uuid, bucket
ORDER BY bucket DESC;


SELECT add_continuous_aggregate_policy('user_physical_activity_yearly',
    start_offset => NULL,
    end_offset   => INTERVAL '1 day',
    schedule_interval => INTERVAL '1 day'
);

DROP  MATERIALIZED VIEW IF EXISTS user_sleep_activity_daily;

CREATE MATERIALIZED VIEW user_sleep_activity_daily
WITH (timescaledb.continuous) AS
SELECT
    user_uuid,
    time_bucket('1 day', start_time) AS bucket,
    SUM(sleep_duration) AS user_sum_sleep_duration,
    AVG(sleep_duration) AS user_avg_sleep_duration,
    LAST(sleep_quality, start_time) AS user_sleep_quality,
    COUNT(*) AS total
FROM sleep_activity
GROUP BY user_uuid, bucket
ORDER BY bucket DESC
;


SELECT add_continuous_aggregate_policy('user_sleep_activity_daily',
    start_offset => INTERVAL '7 day',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 minute'
);

DROP  MATERIALIZED VIEW IF EXISTS user_sleep_activity_monthly;

CREATE MATERIALIZED VIEW user_sleep_activity_monthly
WITH (timescaledb.continuous) AS
SELECT
    user_uuid,
    time_bucket('1 month', start_time) AS bucket,
    SUM(sleep_duration) AS user_sum_sleep_duration,
    AVG(sleep_duration) AS user_avg_sleep_duration,
    LAST(sleep_quality, start_time) AS user_sleep_quality,
    COUNT(*) AS total
FROM sleep_activity
GROUP BY user_uuid, bucket
ORDER BY bucket DESC
;


SELECT add_continuous_aggregate_policy('user_sleep_activity_monthly',
    start_offset => INTERVAL '1 year',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 day'
);

DROP  MATERIALIZED VIEW IF EXISTS user_sleep_activity_yearly;

CREATE MATERIALIZED VIEW user_sleep_activity_yearly
WITH (timescaledb.continuous) AS
SELECT
    user_uuid,
    time_bucket('1 year', start_time) AS bucket,
    SUM(sleep_duration) AS user_sum_sleep_duration,
    AVG(sleep_duration) AS user_avg_sleep_duration,
    LAST(sleep_quality, start_time) AS user_sleep_quality,
    COUNT(*) AS total
FROM sleep_activity
GROUP BY user_uuid, bucket
ORDER BY bucket DESC
;


SELECT add_continuous_aggregate_policy('user_sleep_activity_yearly',
    start_offset => NULL,
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 day'
);


DROP  MATERIALIZED VIEW IF EXISTS user_blood_tests_daily;

CREATE MATERIALIZED VIEW user_blood_tests_daily
WITH (timescaledb.continuous) AS
SELECT
    user_uuid,
    time_bucket('1 day', test_date) AS bucket,
    LAST(glucose_level, test_date) AS user_glucose,
    LAST(cholesterol_level, test_date) AS user_cholesterol,
    LAST(cortisol_level, test_date) AS user_cortisol,
    LAST(melatonin_level, test_date) AS user_melatonin,
    AVG(glucose_level) AS user_avg_glucose,
    AVG(cholesterol_level) AS user_avg_cholesterol,
    AVG(cortisol_level) AS user_avg_cortisol,
    AVG(melatonin_level) AS user_avg_melatonin,
    COUNT(*) AS total
FROM blood_tests
GROUP BY user_uuid, bucket
ORDER BY bucket DESC
;


SELECT add_continuous_aggregate_policy('user_blood_tests_daily',
    start_offset => INTERVAL '1 month',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 day'
);

DROP  MATERIALIZED VIEW IF EXISTS user_blood_tests_monthly;

CREATE MATERIALIZED VIEW user_blood_tests_monthly
WITH (timescaledb.continuous) AS
SELECT
    user_uuid,
    time_bucket('1 month', test_date) AS bucket,
    LAST(glucose_level, test_date) AS user_glucose,
    LAST(cholesterol_level, test_date) AS user_cholesterol,
    LAST(cortisol_level, test_date) AS user_cortisol,
    LAST(melatonin_level, test_date) AS user_melatonin,
    AVG(glucose_level) AS user_avg_glucose,
    AVG(cholesterol_level) AS user_avg_cholesterol,
    AVG(cortisol_level) AS user_avg_cortisol,
    AVG(melatonin_level) AS user_avg_melatonin,
    COUNT(*) AS total
FROM blood_tests
GROUP BY user_uuid, bucket
ORDER BY bucket DESC
;


SELECT add_continuous_aggregate_policy('user_blood_tests_monthly',
    start_offset => INTERVAL '1 year',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 day'
);

DROP  MATERIALIZED VIEW IF EXISTS user_blood_tests_yearly;

CREATE MATERIALIZED VIEW user_blood_tests_yearly
WITH (timescaledb.continuous) AS
SELECT
    user_uuid,
    time_bucket('1 year', test_date) AS bucket,
    LAST(glucose_level, test_date) AS user_glucose,
    LAST(cholesterol_level, test_date) AS user_cholesterol,
    LAST(cortisol_level, test_date) AS user_cortisol,
    LAST(melatonin_level, test_date) AS user_melatonin,
    AVG(glucose_level) AS user_avg_glucose,
    AVG(cholesterol_level) AS user_avg_cholesterol,
    AVG(cortisol_level) AS user_avg_cortisol,
    AVG(melatonin_level) AS user_avg_melatonin,
    COUNT(*) AS total
FROM blood_tests
GROUP BY user_uuid, bucket
ORDER BY bucket DESC
;


SELECT add_continuous_aggregate_policy('user_blood_tests_yearly',
    start_offset => NULL,
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 day'
);

DROP  MATERIALIZED VIEW IF EXISTS user_biometrics_daily;

CREATE MATERIALIZED VIEW user_biometrics_daily
WITH (timescaledb.continuous) AS
SELECT
    user_uuid,
    time_bucket('1 day', recorded) AS bucket,
    LAST(bmi, recorded) AS user_bmi,
    LAST(age, recorded) AS user_age,
    COUNT(*) AS total
FROM biometrics
GROUP BY user_uuid, bucket
ORDER BY bucket DESC;


SELECT add_continuous_aggregate_policy('user_biometrics_daily',
    start_offset => INTERVAL '7 day',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 minute'
	);

DROP  MATERIALIZED VIEW IF EXISTS user_biometrics_monthly;

CREATE MATERIALIZED VIEW user_biometrics_monthly
WITH (timescaledb.continuous) AS
SELECT
    user_uuid,
    time_bucket('1 month', recorded) AS bucket,
    LAST(bmi, recorded) AS user_bmi,
    LAST(age, recorded) AS user_age,
    COUNT(*) AS total
FROM biometrics
GROUP BY user_uuid, bucket
ORDER BY bucket DESC;


SELECT add_continuous_aggregate_policy('user_biometrics_monthly',
    start_offset => INTERVAL '1 year',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 day'
	);

DROP  MATERIALIZED VIEW IF EXISTS user_biometrics_yearly;

CREATE MATERIALIZED VIEW user_biometrics_yearly
WITH (timescaledb.continuous) AS
SELECT
    user_uuid,
    time_bucket('1 year', recorded) AS bucket,
    LAST(bmi, recorded) AS user_bmi,
    LAST(age, recorded) AS user_age,
    COUNT(*) AS total
FROM biometrics
GROUP BY user_uuid, bucket
ORDER BY bucket DESC;


SELECT add_continuous_aggregate_policy('user_biometrics_yearly',
    start_offset => NULL,
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 day'
	);

-- Create a function to refresh continuous aggregates
CREATE OR REPLACE FUNCTION refresh_continuous_aggregates()
RETURNS TRIGGER AS $$
BEGIN
    -- Refresh each continuous aggregate
    CALL refresh_continuous_aggregate('system_avg_biometrics_daily', NULL, NULL);
    CALL refresh_continuous_aggregate('system_avg_biometrics_monthly', NULL, NULL);
    CALL refresh_continuous_aggregate('system_avg_biometrics_yearly', NULL, NULL);
    CALL refresh_continuous_aggregate('system_avg_physical_activity_daily', NULL, NULL);
    CALL refresh_continuous_aggregate('system_avg_physical_activity_monthly', NULL, NULL);
    CALL refresh_continuous_aggregate('system_avg_physical_activity_yearly', NULL, NULL);
    CALL refresh_continuous_aggregate('system_avg_sleep_activity_daily', NULL, NULL);
    CALL refresh_continuous_aggregate('system_avg_sleep_activity_monthly', NULL, NULL);
    CALL refresh_continuous_aggregate('system_avg_sleep_activity_yearly', NULL, NULL);
    CALL refresh_continuous_aggregate('system_avg_blood_tests_daily', NULL, NULL);
    CALL refresh_continuous_aggregate('system_avg_blood_tests_monthly', NULL, NULL);
    CALL refresh_continuous_aggregate('system_avg_blood_tests_yearly', NULL, NULL);
    CALL refresh_continuous_aggregate('user_physical_activity_daily', NULL, NULL);
    CALL refresh_continuous_aggregate('user_physical_activity_monthly', NULL, NULL);
    CALL refresh_continuous_aggregate('user_physical_activity_yearly', NULL, NULL);
    CALL refresh_continuous_aggregate('user_sleep_activity_daily', NULL, NULL);
    CALL refresh_continuous_aggregate('user_sleep_activity_monthly', NULL, NULL);
    CALL refresh_continuous_aggregate('user_sleep_activity_yearly', NULL, NULL);
    CALL refresh_continuous_aggregate('user_blood_tests_daily', NULL, NULL);
    CALL refresh_continuous_aggregate('user_blood_tests_monthly', NULL, NULL);
    CALL refresh_continuous_aggregate('user_blood_tests_yearly', NULL, NULL);
    CALL refresh_continuous_aggregate('user_biometrics_daily', NULL, NULL);
    CALL refresh_continuous_aggregate('user_biometrics_monthly', NULL, NULL);
    CALL refresh_continuous_aggregate('user_biometrics_yearly', NULL, NULL);
END;
$$ LANGUAGE plpgsql;


SELECT cron.schedule(
    'refresh_health_aggregate_every_5_minutes',
    '*/5 * * * *',
    'CALL refresh_continuous_aggregates'
);

SELECT cron.schedule(
    'refresh_daily_health_aggregate',
    '0 1 * * *',
    'CALL refresh_continuous_aggregates'
);
