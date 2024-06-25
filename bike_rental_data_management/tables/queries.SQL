CREATE TABLE date_dim (
	date_key integer PRIMARY KEY,
  full_date date,
  month varchar,
  day integer,
  month_name varchar,
  day_name varchar,
  weekend bool
);

CREATE TABLE stations (
	station_id integer PRIMARY KEY,
  station_name varchar,
  station_latitude integer,
  station_longitude integer
);

CREATE TABLE users(
	id integer PRIMARY KEY,
  birth_year integer,
  age integer,
  user_type varchar(50),
  gender integer
);

CREATE TABLE rides (
	id integer PRIMARY KEY,
  bike_id integer,
  user_id integer,
  start_station_id integer,
  end_station_id integer,
  date_key integer,
  start_time timestamp,
  stop_time timestamp,
  trip_hours integer,
  trip_minutes integer,
  trip_duration integer,
  valid_trip_duration bool,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (date_key) REFERENCES date_dim(date_key),
  FOREIGN KEY (start_station_id) REFERENCES stations(station_id),
  FOREIGN KEY (end_station_id) REFERENCES stations(station_id)
);

CREATE TABLE weather (
	weather_id integer PRIMARY KEY,
  date_key integer,
  avg_wind integer,
  prcp integer,
  snow_amt integer,
  snow_depth integer,
  t_avg integer,
  t_min integer,
  t_max integer,
  rain bool,
  snow bool,
  FOREIGN KEY (date_key) REFERENCES date_dim(date_key)
);

ALTER TABLE rides
ADD valid_trip_duration bool;

SELECT PG_GET_SERIAL_SEQUENCE('"date_dim"', 'date_key');

SELECT CURRVAL(PG_GET_SERIAL_SEQUENCE('"date_dim"', 'date_key')) AS "Current Value", MAX("date_key") AS "Max Value" FROM "date_dim";

SELECT SETVAL((SELECT PG_GET_SERIAL_SEQUENCE('"date_dim"', 'date_key')), (SELECT (MAX("date_key") + 1) FROM "date_dim"), FALSE);