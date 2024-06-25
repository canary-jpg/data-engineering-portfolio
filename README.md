# Data Engineering Portfolio
Hey! My name is Hazel, and I'm excited to share my still developing data engineering portfolio. Within this repository, you'll find a growing catalog of projects completed in various data analytics/engineering courses or self-development exercises, each of which covers essential skills and techniques.

# Projects
## bike_rental_data_management (writeup link)
A relational database with analytics-ready views connecting Citi Bike and weather datasets. This project involved:
* inspecting and cleaning both datasets
* developing a relational database structure
* implementing the database in PostgreSQL and inserting the dataset
* developing flexible analytics-ready views on top of the relational database

## subscriber_cancellations_pipeline (writeup link)
A semi-automated bash&Python pipeline to regularly transform a messy SQLite database into a clean source of truth for an analytics team. The pipeline:
* performs unit tests to confirm data validity
* writes human-readable errors to an error log
* automatically checks and updates changelogs
* updates a production database with clean new data