 ---create daily counts view
CREATE TABLE daily_counts AS
SELECT date_dim.date_key,
    date_dim.full_date,
    date_dim.month_name,
    date_dim.day,
    date_dim.day_name,
    date_dim.weekend,
    COUNT(rides.id) AS total_rides,
    COUNT(users.user_type) FILTER (WHERE users.user_type = 'Subscriber') AS tot_subscriber_rides,
    COUNT(users.user_type) FILTER (WHERE users.user_type = 'Customer') AS tot_customer_rides,
    COUNT(users.user_type) FILTER (WHERE users.user_type = 'Unknown') AS tot_unknown_rides,
    COUNT(rides.valid_trip_duration) FILTER (WHERE NOT rides.valid_trip_duration) AS total_late_returns
FROM rides
RIGHT JOIN date_dim ON date_dim.date_key = rides.date_key
LEFT JOIN users ON rides.user_id = users.user_id
GROUP BY date_dim.date_key
ORDER BY date_dim.date_key;

--- create daily data view
CREATE VIEW daily_data AS 
SELECT daily_counts.date_key,
    daily_counts.full_date,
    daily_counts.month_name,
    daily_counts.day_name,
    daily_counts.total_rides,
    SUM(daily_counts.total_rides) OVER (PARTIION BY  daily_counts.month_name ORDER BY date_dim.date_key) AS monthly_running_total,
    daily_counts.tot_subscriber_rides,
    daily_counts.tot_customer_rides,
    daily_counts.tot_unknown_rides,
    daily_counts.total_late_returns,
    weather.t_min,
    weather.t_max,
    weather.t_avg,
    weather.avg_wind,
    weather.prcp,
    weather.snow_amt,
    weather.rain,
    weather.snow
FROM daily_counts
JOIN weather ON daily_counts.date_key = weather.date_key
ORDER BY daily_counts.date_key;

--- create monthly data view
CREATE VIEW monthly_data AS 
SELECT date_dim.month,
    date_dim.month_name,
    ROUND(AVG(daily.total_rides)) AS avg_daily_rides,
    SUM(daily.total_rides) AS total_daily_rides,
    ROUND(AVG(daily.tot_customer_rides)) AS avg_customer_rides,
    ROUND(AVG(daily.tot_subscriber_rides)) ASD avg_subscriber_rides,
    SUM(daily.tot_unknown_rides) AS total_unknown_rides,
    SUM(daily.total_late_returns) AS tot_late_returns,
    ROUND(AVG(daily.t_avg)) AS avg_temp,
    COUNT(daily.snow) FILTER (WHERE daily.snow) AS days_with_snow,
    COUNT(daily.rain) FILTER (WHERE daily.rain) AS days_with_rain,
    MAX(daily.snow_amt) AS max_snow_amt,
    MAX(daily.prcp) AS max_prcp
FROM date_dim
JOIN daily_data AS daily ON date_dim.date_key = daily.date_key
GROUP BY date_dim.month, date_dim.month_name
ORDER BY date_dim.month, date_dim.month_name;

--- create late returns view
CREATE VIEW late_returns AS 
SELECT date_dim.full_date,
    rides.id,
    rides.trip_hours,
    rides.bike_id,
    (SELECT stations.station_name
    FROM stations
    WHERE rides.start_station_id = stations.station_id) AS start_location,
    (SELECT stations.station_name
    FROM stations
    WHERE rides.end_station_id = stations.station_id) AS end_location,
    users.user_type
FROM rides
JOIN date_dim ON rides.date_key = date_dim.date_key
JOIN users ON rides.user_id = users.user_id
WHERE rides.valid_trip_duration = False;

--- create users view
CREATE VIEW users AS 
SELECT users.user_id,
    users.age,
    users.gender,
    users.user_type,
    COUNT(rides.id) AS total_rides
FROM rides
JOIN users ON rides.user_id = users.user_id
GROUP BY users.user_id, users.age, users.gender, users.user_type
ORDER BY users.user_id, users.age, users.gender, users.user_type;