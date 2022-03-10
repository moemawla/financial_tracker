# drop database tables
cd financial_tracker/
flask db-custom drop

# upgrade and initialize database
flask db upgrade
flask db-custom init

# create directory for database dumps
mkdir database_dumps

exit 0
