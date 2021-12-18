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

<br/>

## Requirements

You need the following:
- Python3 must be installed.
- Pip3 must be installed.
- PostgreSQL must be installed.

<br/>

## Installation steps

    1- Copy ".env.dist" to ".env" file.
    2- Make sure you have a new database created in PostgreSQL with a user that has full access to it.
    3- Set the database name, user and password in ".env" file.
    4- Create a S3 bucket on AWS and create an IAM user that has programatic access to this bucket with permissions to read, write and delete objects from the bucket.
    5- Set the bucket name and credentials in ".env" file.
    6- run the script "install.sh" which will create the virtual environment, install dependencies, create the database tables and initialize the needed data.
    7- Run the following command to fire up the flask web server: "source venv/bin/activate && cd financial_tracker && flask run"

<br/>

## Pages and functionalities

<br/>

### Log In page

![login page](./docs/1.png)

When users first enter the website, they will be redirected to the login page where they can use their email and password to login or, in case they haven't signed-up before, they can click on the "Sign Up" link in the menu.

<br/>

### Sign Up page

![signup page](./docs/2.png)

Users can sign up with their email addresses as long as the email they provide is not used by another account. After the signup details are provided and submitted, the application will create the account, login the user and redirect them to the main page (Transaction Index).

Field validations:
- Name must be provided and should have a minimum length of 1 character.
- Email must be provided and should be of a valid email format.
- Password must be provided and should be at least 6 characters long.

<br/>

### Transaction Index page

![empty transaction index page](./docs/3.png)

After signup/login the users are redirected to the transaction index page. Here users can create new transactions which can be either debit or credit transactions.

Field validations:
- Name must be provided and should have a minimum length of 1 character.
- Amount must be provided and the HTML form input of type "number" will make sure the users only enter numbers, which makes it less likely for them to enter invalid values. It can also be either negative (for credit) or positive (for debit).
- Date must be provided and the HTML form input of type "date" will make sure the users only enter dates, which makes it less likely for them to enter invalid values and much easier to use.

The transaction index page also shows the total balance of the user at the top, in addition to a list of transactions the user has created which are listed at the bottom ordered by the date in ascending order.

![populated transaction index page](./docs/4.png)

<br/>

### Transaction Detail page

![transaction detail page](./docs/5.png)

After creating a transaction, or after clicking on its link in the list, users will be redirected to the transaction detail page. Here they can view/update the details of the transaction, in addition to the ability to add/remove multiple image files that act as proof or as supporting documents for the transaction. The images are stored on an AWS S3 bucket and their names/paths are saved in the database. This page also provides users with the option to delete the transaction, which under the hood also deletes the images from the S3 bucket and their details from the database.

![transaction detail page with images](./docs/6.png)

Field validations:
- Name must be provided and should have a minimum length of 1 character.
- Amount must be provided and the HTML form input of type "number" will make sure the users only enter numbers, which makes it less likely for them to enter invalid values. It can also be either negative (for credit) or positive (for debit).
- Date must be provided and the HTML form input of type "date" will make sure the users only enter dates, which makes it less likely for them to enter invalid values and much easier to use.

<br/>

### Account Details page

![account details page](./docs/7.png)

When pressing the "Account" link in the menu, users will be redirected to the account details page. Here users can view/update their name and email, in addition to the address details. The address details are initially empty, but once the user updates them an address will be created for the user and saved to the database. In addition, the address details section includes a drop down containing the list of all countries which can be managed from the database by setting certain countries as active/inactive.

![account details page with address](./docs/8.png)

Field validations for account details:
- Name must be provided and should have a minimum length of 1 character.
- Email must be provided and should be of a valid email format. The email should also be unique, where a user cannot update the email to something that is used by a different account.

Field validations for address details:
- Street name must be provided and should have a minimum length of 1 character.
- Suburb name must be provided and should have a minimum length of 1 character.
- State name must be provided and should have a minimum length of 1 character.
- Country must be provided and the HTML form input of type "select" will make it much easier for users to enter the correct value for the country they intend.

<br/>

