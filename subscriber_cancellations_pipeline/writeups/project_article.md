# Project Writeup
A semi-automated bash & Python pipeline to regularly transform a messy SQLite database into a clean source of truth for an analytics team.
The pipeline:
* performs unit tests to confirm data validity
* writes human-readable errors to an error log
* automatically checks and updates changelogs
* updates a production database with clean new data

## Scenario
A fictional online education company, Cademycode, has a database of cancelled subscriber information that gets periodically updated from a variety of sources. They want to automate the process of transforming this messy database into a clean table for their analytics team. My goal was to create a semi-automated data ingestion pipeline that checks for new data, automatically performs cleaning and transformation operations, runs unit tests to check data validity, and logs errors for human review.

## The Process
### Inspecting and Transforming the Dataset
To begin the process, there were several of the raw data tables with incomplete data. Visualizations indicated that most of the data was missing at random (MAR). Because the data was MAR and formed only a small percentage of the overall data, deletion seemed most appropriate. Instead of completely deleting the missing rows, I separated the rows with missing data into their own table. This way, an analytics team can inspect the missing data themselves if they want to, and we can keep track of how much data is missing as the cleaned database continues to get updated. 
Some of the missing data was structurally missing, corresponding to students who hadn't started any courses before cancelling their subscriptions. I handled these rows by creating a new column for those students, so an analytics team can easily study subscribers who cancel before starting any courses.
In addition to missing data, the student's contact information was stored in a dictionary, which needed to be converted to flat columns with the correct datatypes.
Lastly, I added new columns to assist an analytics team in filtering the subscriber population. For example, I used the subscriber's birth data to create age and decade categories, so an analytics team can more easily see if those demographic attributes impact subscribers.

### Automation
Because the raw database is updated regularly with new long-term cancellations, the transformations discussed above need to be automated as much as possible. However, an automated data process also needs automated checks to prevent unwanted data updates. Therefore, the cleaning and wrangling code need to be wrapped in a Python script to perform unit tests, log errors, and track any features of potential concern (eg. a sudden increase in records with missing rows).
My unit tests check:
* if there are any updates to the database
* if there are any new rows with missing values in the updates
* if the table schemas are the same as expected
* if all join keys are present between the tables before joining
If the process passses all the tests, I can be reasonably confident that the automated cleaning script will operate as I excepted from my Jupyter notebook, and the update can proceed. If not, then logged errors will help me identify any unexpected changes to the database (for example, a new column) that my script wasn't designed to handle. Even if all the unit tests are successful, the script still records data regarding missing records to the changelog for human review.
Lastly, I created a bash script to automate the process of:
1. running the unit tests and updating the script
2. checking if the script found and made any updates
3. if so, moving the newly updated clean database to a production folder