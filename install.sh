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

# install pip3 and nginx
sudo apt update
sudo apt install -y python3-pip
sudo apt install -y nginx

# get the absolute path to the directory containing this script
dir_path=$(dirname $(realpath $0))

# install requirements
sudo pip3 install -r $dir_path/requirements.txt


# setup gunicorn process
sudo cp $dir_path/financial_tracker_app.service /etc/systemd/system/financial_tracker_app.service
sudo systemctl daemon-reload
sudo systemctl start financial_tracker_app
sudo systemctl enable financial_tracker_app

# setup nginx
sudo systemctl start nginx
sudo systemctl enable nginx
sudo cp $dir_path/nginx.config /etc/nginx/sites-available/default
sudo systemctl restart nginx

exit 0
