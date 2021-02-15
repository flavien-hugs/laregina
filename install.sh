#!/usr/bin/env bash
echo "***********************************************"
echo "***************** install *********************"
echo "***********************************************"

echo "***********************************************"
echo "---apt update e upgrade---"
echo "***********************************************"
apt-get -y update

echo "***********************************************"
echo "---OS dependencies---"
echo "***********************************************"
apt-get -y install python3-pip
apt-get -y install python3-dev python3-setuptools
apt-get -y install git
apt-get -y install virtualenv

# .....
# .....
# .....
# .....

echo "***********************************************"
echo "--- install dependencies (including django) ---"
echo "***********************************************"
pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
