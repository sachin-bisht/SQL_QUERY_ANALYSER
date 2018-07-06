# SQL QUERY ANALAYSER
SQL query analayser analyse the given python file by the user and do the following.

1. List all the queries.
2. Checking if the table exists.
3. Checking if the column exists.
4. Execute an 'explain' on queries and listing indexes for each query
5. Smart Suggestion

	For each table - suggesting new indexes and also telling which indexes isn't useful. [Reducing time complexity]
6. Send the report to the given email_id.

## Prerequisites
1. MySQL
2. Python3
3. PyMySQL


## How to run
1. Insert the file which you want to analyse in the search_file directory.
2. Run **drive.py** and enter the filename for which you want to generate the report. Also enter the EmailId to send the report.

