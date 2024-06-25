# Bike Rental Data Management
This repository contains code for the `Bike Rental Data Management` project

## Project Overview
This goal of this project was to create a relational database with analytics-ready views connecting Citi Bike and weather datasets. The project involved:
* inspecting and cleaning both datasets
* developing a relational database structure
* implementing the database in PostgreSQL and inserting the dataset
* developing flexible analytics-ready views on top of the relational database

# Folder Structure
* bike_rental.ipynb: Jupyter Notebook detailing how I prepared the data for inserting into the database
* writeup.md: A markdown file going into detail about the logic behind my process 

## `tables`
* tables.SQL: SQL queries to create database tables
* views.SQL: SQL queries to create database views
* queries.SQL: SQL queries to establish data types and relationships of each of the tables
* bike_rental_erd.pdf: Entity relationship diagram for the database

## `data`
* newark_airport_2016.csv: Weather data from Newark Airport
* JC-2016xx-citibike-tripdata.csv: Twelve files containing one month of Citi Bike data from Jersey City
    ** replace `xx` with the number of each month

## `data-dictionaries`
* citibike.pdf: Details on the Citi Bike data files from Citi Bike's website
* weather.pdf: Details on the weather data from NOAA's website
