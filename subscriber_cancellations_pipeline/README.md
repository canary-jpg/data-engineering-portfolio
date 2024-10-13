# Subscriber Cancellations Data Pipeline Project

This repository contains code for the Subscriber Cancellations Data Pipeline.

## Project Description
This project is a semi-automated bash & Python to regularly transform a messy SQLite database into a clean source of truth for an analytics team.
The pipeline
* performs unit tests to confirm data validity
* writes human-readable errors to an error log
* automatically checks and updates changelogs
* updates the production database with new clean data

Please see writeup/article.md for an overview of the development process and writeup/cleaning-subsriber-data.ipynb for an exploratory Jupyter notebook.

### Instructions
This repo is set up as if the scripts have never been run. To properly run:

1. Run script.sh and follow the prompts
2. If prompted, script.sh will run dev.cleanse_data.py, which runs unit tests and data cleaning functions on dev/cademycode.db
3. If cleanse_data.py runs into any errors during unit testing, it will raise an exception, log the issue, and terminate
4. Otherwise, clease_data.py will update the clean database and CSV with any new records
5. After a successful update, the number of new records and other updated data will be written to dev/changelog.md
6. script.sh will check the changelog to see if there are updates
7. If so, script.sh will request permission to overwrite the production database
8. If the user grants permission, script.sh will copy the updated database to prod

If you follow these instructions, the script will run on the initial dataset in dev/cademycode.db. To tests running the script on the updated database, change the name of dev/cademycode.db to dev/cademycode_updated.db

## Folder Structure
* script.sh: the bash script to handle runnning the data cleanser and moving files to /prod

#### dev
* changlog.md: automatically updated for each run, logs new records and tracks missing data
* cleanse_data.py: runs unit tests and cleansing on cademycode.db
* cleanse_db.log: logs errors encountered during python script execution
* cademycode_updated.db: output from cleanse_data.py that contains two tables
    * cademycode_aggreagted: a table containing the joined data from cleansed version of three cademycode.db tables
    * missing_data: a table containing incomplete data that could not imputed or assumed
* cademycode.db: database containing data from three raw tables:
    * cademycode_students: table containing student demographic and course information from cademycode
    * cademycode_student_jobs: a lookup table containing student job industries
    * cademycode_courses: a lookup table containing career paths and number of hours it takes to complete each course
* cademycode_updated.db: database used for testing the update process

### prod
* changelog.md: script.sh will copy from /dev when updates are approved
* cademycode_cleansed.db: script.sh will copy from /dev when updates are approved
* cademycode_cleansed.csv:  CSV version of the clean table, overwritten upon update

### writeup
* article.md: a high-level overview of the project detailing the process of developing these scripts
* cleaning-subscriber-data.ipynb: Jupyter notebook containing the discovery phase of this project

