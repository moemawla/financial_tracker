#!/bin/bash

# check if Python 3 is installed
version="$(python3 -V 2>&1)"
if [[ $version != "Python 3"* ]]
then
    version="$(python -V 2>&1)"
    if [[ $version != "Python 3"* ]]
    then
        echo 'Error: You dont have Python 3 installed' >&2
        exit 1
    fi
fi

# check if pip is installed
version="$(pip3 -V 2>&1)"
if [[ $version != "pip"* ]]
then
    echo 'Error: You dont have pip installed' >&2
    exit 1
fi

# get the absolute path to the directory containing this script
dir_path=$(dirname $(realpath $0))

# install requirements
pip3 install -r $dir_path/requirements.txt

# drop database tables
cd financial_tracker/
flask db-custom drop

# upgrade and initialize database
flask db upgrade
flask db-custom init

# create directory for database dumps
mkdir database_dumps

exit 0
