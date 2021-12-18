# Financial Tracker

## Overview

This application is a web-based financial tracker. The users can manage their income and expenses through the application to track their financials and make better decisions. 

Users are able to perform the following:
- sign-up.
- login/logout.
- edit profile and add/update address.
- manage income/expense transactions (create, view, update, delete).
- add/remove multiple supporting images for each transaction.
- view total balance and list of all transactions ordered by date.


## Requirements

You need the following:
- Python3 must be installed.
- Pip3 must be installed.
- PostgreSQL must be installed.


## Installation steps

    1- Copy ".env.dist" to ".env" file.
    2- Make sure you have a new database created in PostgreSQL with a user that has full access to it.
    3- Set the database name, user and password in ".env" file.
    4- Create a S3 bucket on AWS and create an IAM user that has programatic access to this bucket with permissions to read, write and delete objects from the bucket.
    5- Set the bucket name and credentials in ".env" file.
    6- run the script "install.sh" which will create the virtual environment, install dependencies, create the database tables and initialize the needed data.
    7- Run the following command to fire up the flask web server: "source venv/bin/activate && cd financial_tracker && flask run"


## Pages and functionalities


