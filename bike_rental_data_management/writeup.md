# Bike Rental Data Management Writeup

# Project Overview
During the last decade, we have seen enormous growth in the personal transportation industry, including bike rental programs in major cities nationwide. This project aimed to create a flexible and efficient database to store information about bike rental data using Citi Bike and NOAA datasets. This project involved:
inspecting and cleaning the datasets
developing a relational database structure
implementing the database into POSTGRESQL and inserting the data
developing analytic ready views on top of the relational database

## Inspecting and Cleaning the Datasets
Our first step was the meticulous inspection and cleaning of the datasets.
The datasets used in this project were monthly Citi Bike trip records and daily NOAA data from Newark Airport. All the datasets were from 2016. 
The Citi Bike datasets presented a few data integrity issues. Specifically, some fields such as user type and birth year had missing values. Further analysis revealed that this data was not missing at random, with demographic information for non-customers being almost entirely absent. To address this, I preserved the missing data, labeling those users as unknown, and created summary columns for easy use or removal of the missing data as required. This process was crucial in assisting the analytic team in their investigation of this issue. 
There were also some outliers in some of the numeric fields. For example, the trip duration column has trips from thousands of hours; even the maximum trip duration for Citi Bikes is only 24 hours. Since these values could indicate a system malfunction or users keeping the bikes past their rental time, I kept them in the dataset. I created a flag detailing each ride's valid trip duration (to easily keep or remove them from any future analysis). I also added columns detailing the number of trip minutes and trip hours. 
The weather dataset has some null values that need to be dropped, leaving the wind speed, precipitation, temperature, snow depth, and snow amount. I created binaries for snow and rain indicators to assist in filtering views. 

## Developing a Relational Database Structure
The Citi Bike dataset required adjustments to get the needed tables; for example, I separated the user demographic and station information into two unique tables. The station data already had an ID column that used a primary key. At the same time, the user information needed a new primary key and pointers added to the original Citi Bike data.
The weather data required less restructuring, but using dates as a primary key is risky. To facilitate joins, I create a date_key  field for the weather and Citi Bike data that stores each date as an integer in the yyyymmdd format. 
Finally, I created a date dimension table to store date information more efficiently. The table stores information about each day as both a date and an integer date_key along with:
month as both a number and a name
day as both a number and name
whether the day is the weekend or not
Based on these tables, I created a database schema specifying data types and primary/foreign key relationships. After creating the database in PostgreSQL that matches the schema, I inserted the data into their respective tables using SQLAlchemy and Pandas.

## Developing Views
To assist the analytics team, I created the following views:

###`daily_data`
The view contains data from each day of the year (I  used outer joins to ensure the analytic team can investigate the days missing from the Citi Bike data). In addition to total rides on a given day, the view contains:
date breakdowns (month and day of the week),
ride breakdowns (using filter statements based on user types and trip duration)
running month totals (using window functions)
and weather data 
This view contains information about the unknown user types and the suspiciously large trip duration, which the analytics team will use to investigate these issues more closely.
### `monthly_data`
This view summarizes the daily_data by month. In addition to the number of months per ride, it contains
total number of rides based on user type
daily number of rides based on user type
average temperature and maximum snow amounts/rain inches
counts of snow days and rain days
### `users`
In addition to monthly and daily data, I created a user table to get basic demographic information about each rider.
