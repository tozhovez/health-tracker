CALL refresh_continuous_aggregate('system_avg_biometrics_daily', NULL, NULL);
CALL refresh_continuous_aggregate('system_avg_physical_activity', NULL, NULL);
CALL refresh_continuous_aggregate('system_avg_sleep_activity', NULL, NULL);
CALL refresh_continuous_aggregate('system_avg_blood_tests', NULL, NULL);
CALL refresh_continuous_aggregate('user_physical_activity', NULL, NULL);
CALL refresh_continuous_aggregate('user_sleep_activity', NULL, NULL);
CALL refresh_continuous_aggregate('user_blood_tests', NULL, NULL);
CALL refresh_continuous_aggregate('user_biometrics', NULL, NULL);


SELECT add_continuous_aggregate_policy('system_avg_sleep_activity',
    start_offset => INTERVAL '7 day',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 minute'
);

SELECT add_continuous_aggregate_policy('system_avg_biometrics_daily',
    start_offset => INTERVAL '7 day',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 minute'
);

SELECT add_continuous_aggregate_policy('system_avg_physical_activity',
    start_offset => INTERVAL '7 day',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 minute'
);
SELECT add_continuous_aggregate_policy('system_avg_blood_tests',
    start_offset => INTERVAL '7 day',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 minute'
);

SELECT add_continuous_aggregate_policy('user_physical_activity',
    start_offset => INTERVAL '1 month',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 minute'
);


SELECT add_continuous_aggregate_policy('user_sleep_activity',
    start_offset => INTERVAL '7 day',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 minute'
);


SELECT add_continuous_aggregate_policy('user_blood_tests',
    start_offset => INTERVAL '7 day',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 minute'
);


SELECT add_continuous_aggregate_policy('user_biometrics',
    start_offset => INTERVAL '7 day',
    end_offset   => INTERVAL '1 second',
    schedule_interval => INTERVAL '1 minute'
	);