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

# check and install virtualenv
version="$(virtualenv --version 2>&1)"
if [[ $version != "virtualenv"* ]]
then
    pip3 install virtualenv
fi

# get the absolute path to the directory containing this script
dir_path=$(dirname $(realpath $0))

# create and activate the virtual environment
rm -rf $dir_path/venv
virtualenv $dir_path/venv
source $dir_path/venv/bin/activate

# install requirements
pip3 install -r $dir_path/requirements.txt

exit 0
